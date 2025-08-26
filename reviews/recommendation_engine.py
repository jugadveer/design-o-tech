import re
from collections import Counter
from .models import Item, Review, Recommendation
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        pass
    
    def get_user_preferences(self, user):
        reviews = Review.objects.filter(user=user)
        
        if not reviews.exists():
            return {
                'liked_categories': [],
                'sentiment_preferences': {}
            }
        
        category_sentiments = {}
        liked_categories = set()
        
        for review in reviews:
            category = review.category
            sentiment = review.sentiment
            
            if category not in category_sentiments:
                category_sentiments[category] = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            if sentiment:
                category_sentiments[category][sentiment] += 1
                if sentiment == 'positive':
                    liked_categories.add(category)
            else:
                category_sentiments[category]['neutral'] += 1
        
        sentiment_preferences = {}
        for category, sentiments in category_sentiments.items():
            total = sum(sentiments.values())
            if total > 0:
                positive_ratio = sentiments['positive'] / total
                if positive_ratio > 0.5:
                    liked_categories.add(category)
                sentiment_preferences[category] = positive_ratio
        
        return {
            'liked_categories': list(liked_categories),
            'sentiment_preferences': sentiment_preferences
        }
    
    def generate_recommendations(self, user, limit=5):
        try:
            user_preferences = self.get_user_preferences(user)
            liked_categories = user_preferences['liked_categories']
            
            recommendations = []
            
            if not liked_categories:
                items = Item.objects.filter(rating__gte=4.0).order_by('-rating')[:limit]
                for item in items:
                    reason = f"Trending! This {item.get_category_display().lower()} item has a {item.rating}/5 rating."
                    base_score = item.rating / 5.0
                    final_score = min(1.0, base_score)
                    
                    recommendation, created = Recommendation.objects.get_or_create(
                        user=user,
                        item=item,
                        defaults={
                            'score': final_score,
                            'reason': reason
                        }
                    )
                    
                    if not created:
                        recommendation.score = final_score
                        recommendation.reason = reason
                        recommendation.save()
                    
                    recommendations.append(recommendation)
            else:
                items_from_liked = Item.objects.filter(
                    category__in=liked_categories,
                    rating__gte=3.5
                ).order_by('-rating')[:limit//2]
                
                items_from_other = Item.objects.exclude(
                    category__in=liked_categories
                ).filter(rating__gte=4.0).order_by('-rating')[:limit//2]
                
                items = list(items_from_liked) + list(items_from_other)
                
                if len(items) < limit:
                    remaining = limit - len(items)
                    additional_items = Item.objects.filter(rating__gte=4.0).exclude(
                        id__in=[item.id for item in items]
                    ).order_by('-rating')[:remaining]
                    items.extend(additional_items)
                
                if len(items) < limit:
                    remaining = limit - len(items)
                    popular_items = Item.objects.filter(rating__gte=4.5).exclude(
                        id__in=[item.id for item in items]
                    ).order_by('-rating')[:remaining]
                    items.extend(popular_items)
                
                for item in items:
                    if item.category in liked_categories:
                        reason = f"Perfect match! Based on your {item.get_category_display().lower()} preferences - rated {item.rating}/5."
                    else:
                        reason = f"Discover something new! This {item.get_category_display().lower()} item is highly rated at {item.rating}/5."
                    
                    base_score = item.rating / 5.0
                    category_boost = 0.1 if item.category in liked_categories else 0
                    final_score = min(1.0, base_score + category_boost)
                    
                    recommendation, created = Recommendation.objects.get_or_create(
                        user=user,
                        item=item,
                        defaults={
                            'score': final_score,
                            'reason': reason
                        }
                    )
                    
                    if not created:
                        recommendation.score = final_score
                        recommendation.reason = reason
                        recommendation.save()
                    
                    recommendations.append(recommendation)
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user.id}: {e}")
            return []
    
    def get_recommendations_for_user(self, user, limit=5):
        recent_recommendations = Recommendation.objects.filter(
            user=user
        ).order_by('-created_at')[:limit]
        
        if not recent_recommendations.exists():
            return self.generate_recommendations(user, limit)
        
        return list(recent_recommendations)
    
    def refresh_recommendations(self, user, limit=5):
        Recommendation.objects.filter(user=user).delete()
        return self.generate_recommendations(user, limit)
    
    def get_diverse_recommendations(self, user, limit=5):
        user_preferences = self.get_user_preferences(user)
        liked_categories = user_preferences['liked_categories']
        
        recommendations = []
        
        if not liked_categories:
            items = Item.objects.filter(rating__gte=4.0).order_by('?')[:limit]
        else:
            items_from_liked = Item.objects.filter(
                category__in=liked_categories,
                rating__gte=3.5
            ).order_by('?')[:limit//2]
            
            items_from_other = Item.objects.exclude(
                category__in=liked_categories
            ).filter(rating__gte=4.0).order_by('?')[:limit//2]
            
            items = list(items_from_liked) + list(items_from_other)
            
            if len(items) < limit:
                remaining = limit - len(items)
                additional_items = Item.objects.filter(rating__gte=4.0).exclude(
                    id__in=[item.id for item in items]
                ).order_by('?')[:remaining]
                items.extend(additional_items)
        
        for item in items:
            if item.category in liked_categories:
                reason = f"Perfect match! Based on your {item.get_category_display().lower()} preferences - rated {item.rating}/5."
            else:
                reason = f"Discover something new! This {item.get_category_display().lower()} item is highly rated at {item.rating}/5."
            
            base_score = item.rating / 5.0
            category_boost = 0.1 if item.category in liked_categories else 0
            final_score = min(1.0, base_score + category_boost)
            
            recommendation, created = Recommendation.objects.get_or_create(
                user=user,
                item=item,
                defaults={
                    'score': final_score,
                    'reason': reason
                }
            )
            
            if not created:
                recommendation.score = final_score
                recommendation.reason = reason
                recommendation.save()
            
            recommendations.append(recommendation)
        
        return recommendations[:limit]

