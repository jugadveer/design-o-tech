from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import Review, AnalysisResult, Item, Recommendation
from .recommendation_engine import RecommendationEngine
import json
import re
from django.db import models
from importlib import import_module
from pathlib import Path


PRIMARY_BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
YELLOW = "#FACC15"


def _nlp():
    return import_module('reviews.nlp')


def _generate_wordcloud(text: str) -> None:
    _nlp().generate_wordcloud(text, Path("static/wordcloud.png"))


@login_required
def review_input(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Get form data
        category = request.POST.get("category", "")
        raw_text = request.POST.get("reviews_text", "").strip()
        uploaded_file = request.FILES.get("reviews_file")
        
        # Combine text from both sources
        combined_text = raw_text
        if uploaded_file and uploaded_file.name.lower().endswith(".txt"):
            combined_text += "\n" + uploaded_file.read().decode("utf-8", errors="ignore")

        # Split into reviews by double newlines or line by line if short
        chunks = [c.strip() for c in re.split(r"\n\n+", combined_text) if c.strip()]
        if len(chunks) < 2:
            chunks = [c.strip() for c in combined_text.splitlines() if c.strip()]

        all_text = []
        reviews_to_create = []
        analysis_results_to_create = []
        
        for chunk in chunks:
            # Analyze sentiment first
            result = _nlp().analyze_text(chunk)
            
            # Create review with sentiment already analyzed
            review = Review(
                user=request.user,
                category=category,
                raw_text=chunk,
                sentiment=result["sentiment"],
                score=result["polarity"]
            )
            reviews_to_create.append(review)
            
            # Prepare analysis result
            analysis_result = AnalysisResult(
                sentiment=result["sentiment"],
                polarity=result["polarity"],
                subjectivity=result["subjectivity"],
                emotion=result["emotion"],
            )
            analysis_results_to_create.append(analysis_result)
            
            all_text.append(chunk)
        
        # Bulk create reviews
        Review.objects.bulk_create(reviews_to_create)
        
        # Get the created reviews and link them to analysis results
        created_reviews = Review.objects.filter(
            user=request.user,
            category=category,
            raw_text__in=all_text
        ).order_by('-created_at')[:len(reviews_to_create)]
        
        # Link analysis results to reviews
        for i, analysis_result in enumerate(analysis_results_to_create):
            if i < len(created_reviews):
                analysis_result.review = created_reviews[i]
        
        # Bulk create analysis results
        AnalysisResult.objects.bulk_create(analysis_results_to_create)
        
        # Generate wordcloud asynchronously (optional)
        try:
            _generate_wordcloud("\n".join(all_text))
        except:
            pass  # Don't block on wordcloud generation
        
        # Clear existing recommendations to force refresh
        Recommendation.objects.filter(user=request.user).delete()
        
        return HttpResponseRedirect(reverse('dashboard') + "?refresh=true")

    return render(request, "review_input.html")


@login_required
def dashboard(request):
    user = request.user
    
    # Check if we need to auto-refresh recommendations (after new review)
    auto_refresh = request.GET.get('refresh', 'false') == 'true'
    
    reviews = Review.objects.filter(user=user)
    total_reviews = reviews.count()
    
    analysis_results = AnalysisResult.objects.filter(review__user=user)
    
    positive_count = analysis_results.filter(sentiment='positive').count()
    negative_count = analysis_results.filter(sentiment='negative').count()
    neutral_count = analysis_results.filter(sentiment='neutral').count()
    
    positive_pct = round((positive_count / total_reviews * 100) if total_reviews > 0 else 0, 1)
    negative_pct = round((negative_count / total_reviews * 100) if total_reviews > 0 else 0, 1)
    neutral_pct = round((neutral_count / total_reviews * 100) if total_reviews > 0 else 0, 1)
    
    # Get sentiment counts for chart
    sentiment_counts = [positive_count, negative_count, neutral_count]
    
    word_freq = {}
    for review in reviews:
        words = review.raw_text.lower().split()
        for word in words:
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
    
    recommendation_engine = RecommendationEngine()
    
    # Auto-refresh recommendations if needed
    if auto_refresh or not Recommendation.objects.filter(user=user).exists():
        # Clear existing recommendations first to avoid duplicates
        Recommendation.objects.filter(user=user).delete()
        recommendations = recommendation_engine.get_diverse_recommendations(user, limit=5)
    else:
        recommendations = recommendation_engine.get_recommendations_for_user(user, limit=5)
    
    recommended_items = [rec.item for rec in recommendations]
    
    if recommendations:
        rec_title = "Personalized Recommendations"
        rec_description = f"Based on your {total_reviews} reviews and preferences"
    else:
        rec_title = "No Recommendations Yet"
        rec_description = "Start adding reviews to get personalized item recommendations"
    
    avg_polarity = round(analysis_results.aggregate(avg=models.Avg('polarity'))['avg'] or 0, 1)
    
    context = {
        'total_reviews': total_reviews,
        'positive_pct': positive_pct,
        'negative_pct': negative_pct,
        'neutral_pct': neutral_pct,
        'sentiment_counts': sentiment_counts,
        'top_words': top_words,
        'recommendations': recommendations,
        'recommended_items': recommended_items,
        'rec_title': rec_title,
        'rec_description': rec_description,
        'avg_rating': avg_polarity,
        'auto_refresh': auto_refresh,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    user = request.user
    
    reviews = Review.objects.filter(user=user).order_by('-created_at')
    
    categories = reviews.values_list('category', flat=True).distinct()
    category_stats = {}
    
    for category in categories:
        category_reviews = reviews.filter(category=category)
        positive_count = category_reviews.filter(sentiment='positive').count()
        total_count = category_reviews.count()
        category_stats[category] = {
            'total': total_count,
            'positive': positive_count,
            'positive_pct': round((positive_count / total_count * 100) if total_count > 0 else 0, 1)
        }
    
    recommendations = Recommendation.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'reviews': reviews,
        'category_stats': category_stats,
        'recommendations': recommendations,
        'total_reviews': reviews.count(),
    }
    
    return render(request, 'profile.html', context)


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")


def landing(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing.html")


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("dashboard")
        else:
            # If form is invalid, redirect back to home with error
            return redirect("home")
    return redirect("home")


def login_view(request: HttpRequest) -> HttpResponse:
    """Handle login form submission from modal"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                # Invalid credentials, redirect to home
                return redirect("home")
        else:
            # Missing credentials, redirect to home
            return redirect("home")
    
    # GET request, redirect to home
    return redirect("home")


def analyze_sentiment(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if not text:
            return JsonResponse({"error": "Text is required"}, status=400)
        
        try:
            result = _nlp().analyze_text(text)
            return JsonResponse({
                "sentiment": result["sentiment"],
                "polarity": result["polarity"],
                "subjectivity": result["subjectivity"],
                "emotion": result["emotion"]
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "POST method required"}, status=405)


def logout_view(request: HttpRequest) -> HttpResponse:
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')


@login_required
def get_recommendations(request):
    """API endpoint to get recommendations for a user"""
    try:
        user = request.user
        limit = int(request.GET.get('limit', 5))
        
        recommendation_engine = RecommendationEngine()
        recommendations = recommendation_engine.get_recommendations_for_user(user, limit=limit)
        
        # Format recommendations for JSON response
        rec_data = []
        for rec in recommendations:
            rec_data.append({
                'id': rec.item.id,
                'name': rec.item.name,
                'description': rec.item.description,
                'category': rec.item.get_category_display(),
                'price': float(rec.item.price),
                'rating': rec.item.rating,
                'image_url': rec.item.image_url,
                'score': rec.score,
                'reason': rec.reason
            })
        
        return JsonResponse({
            'success': True,
            'recommendations': rec_data,
            'count': len(rec_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def refresh_recommendations(request):
    """API endpoint to force refresh recommendations"""
    try:
        user = request.user
        limit = int(request.GET.get('limit', 5))
        
        # Clear existing recommendations
        Recommendation.objects.filter(user=user).delete()
        
        # Generate new diverse recommendations
        recommendation_engine = RecommendationEngine()
        recommendations = recommendation_engine.get_diverse_recommendations(user, limit=limit)
        
        return JsonResponse({
            'success': True,
            'message': f'Generated {len(recommendations)} new recommendations',
            'count': len(recommendations)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
