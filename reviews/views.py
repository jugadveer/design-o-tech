from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Review, AnalysisResult, Product, Recommendation
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
        pasted_text = request.POST.get("reviews_text", "").strip()
        uploaded_file = request.FILES.get("reviews_file")
        combined_text = pasted_text
        if uploaded_file and uploaded_file.name.lower().endswith(".txt"):
            combined_text += "\n" + uploaded_file.read().decode("utf-8", errors="ignore")

        # Split into reviews by double newlines or line by line if short
        chunks = [c.strip() for c in re.split(r"\n\n+", combined_text) if c.strip()]
        if len(chunks) < 2:
            chunks = [c.strip() for c in combined_text.splitlines() if c.strip()]

        all_text = []
        for chunk in chunks:
            review = Review.objects.create(raw_text=chunk)
            result = _nlp().analyze_text(chunk)
            AnalysisResult.objects.create(
                review=review,
                sentiment=result["sentiment"],
                polarity=result["polarity"],
                subjectivity=result["subjectivity"],
                emotion=result["emotion"],
            )
            all_text.append(chunk)

        _generate_wordcloud("\n".join(all_text))
        return redirect("dashboard")

    return render(request, "review_input.html")


@login_required
def dashboard(request):
    """Dashboard view with sentiment analysis and recommendations"""
    user = request.user
    
    # Get all reviews (since Review model doesn't have user field)
    reviews = Review.objects.all()
    total_reviews = reviews.count()
    
    # Get analysis results for sentiment calculation
    analysis_results = AnalysisResult.objects.all()
    
    # Calculate sentiment percentages
    positive_count = analysis_results.filter(sentiment='positive').count()
    negative_count = analysis_results.filter(sentiment='negative').count()
    neutral_count = analysis_results.filter(sentiment='neutral').count()
    
    positive_pct = round((positive_count / total_reviews * 100) if total_reviews > 0 else 0, 1)
    negative_pct = round((negative_count / total_reviews * 100) if total_reviews > 0 else 0, 1)
    neutral_pct = round((neutral_count / total_reviews * 100) if total_reviews > 0 else 0, 1)
    
    # Get sentiment counts for chart
    sentiment_counts = [positive_count, negative_count, neutral_count]
    
    # Get word frequency for word cloud
    word_freq = {}
    for review in reviews:
        words = review.raw_text.lower().split()
        for word in words:
            if len(word) > 3:  # Only count words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top words (limit to 20)
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
    
    # Get recommendations
    recommendation_engine = RecommendationEngine()
    recommendations = recommendation_engine.get_recommendations_for_user(user, limit=5)
    
    # Get recommended products
    recommended_products = [rec.product for rec in recommendations]
    
    # Generate recommendation insights
    if recommendations:
        rec_title = "Personalized Recommendations"
        rec_description = f"Based on your {total_reviews} reviews and preferences"
    else:
        rec_title = "No Recommendations Yet"
        rec_description = "Start adding reviews to get personalized product recommendations"
    
    # Calculate average polarity (since Review doesn't have rating field)
    avg_polarity = round(analysis_results.aggregate(avg=models.Avg('polarity'))['avg'] or 0, 1)
    
    context = {
        'total_reviews': total_reviews,
        'positive_pct': positive_pct,
        'negative_pct': negative_pct,
        'neutral_pct': neutral_pct,
        'sentiment_counts': sentiment_counts,
        'top_words': top_words,
        'recommendations': recommendations,
        'recommended_products': recommended_products,
        'rec_title': rec_title,
        'rec_description': rec_description,
        'avg_rating': avg_polarity,  # Using polarity as rating
    }
    
    return render(request, 'dashboard.html', context)


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
                'id': rec.product.id,
                'name': rec.product.name,
                'description': rec.product.description,
                'category': rec.product.get_category_display(),
                'price': float(rec.product.price),
                'rating': rec.product.rating,
                'image_url': rec.product.image_url,
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
        
        # Generate new recommendations
        recommendation_engine = RecommendationEngine()
        recommendations = recommendation_engine.generate_recommendations(user, limit=limit)
        
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
