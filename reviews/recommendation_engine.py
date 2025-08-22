import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Product, Review, Recommendation
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.9
        )
    
    def extract_keywords_from_reviews(self, reviews):
        """Extract keywords from user reviews"""
        if not reviews:
            return []
        
        # Combine all review text
        all_text = ' '.join([review.raw_text for review in reviews])
        
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]+\b', all_text.lower())
        
        # Remove common words and short words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs'
        }
        
        # Filter words
        filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Get most common words
        word_counts = Counter(filtered_words)
        keywords = [word for word, count in word_counts.most_common(20)]
        
        return keywords
    
    def get_user_preferences(self, user):
        """Get user preferences based on their reviews"""
        # Since Review model doesn't have user field, get all reviews
        reviews = Review.objects.all()
        
        if not reviews.exists():
            return {
                'keywords': [],
                'categories': [],
                'sentiment_preferences': {}
            }
        
        # Extract keywords
        keywords = self.extract_keywords_from_reviews(reviews)
        
        # Get category preferences
        category_counts = Counter()
        sentiment_by_category = {}
        
        for review in reviews:
            # Analyze sentiment for each review
            try:
                from .nlp import analyze_text
                analysis = analyze_text(review.raw_text)
                
                # Count categories mentioned in reviews
                # This is a simple approach - in a real system you'd use NER
                review_lower = review.raw_text.lower()
                for category in Product.CATEGORY_CHOICES:
                    category_name = category[0]
                    if category_name in review_lower:
                        category_counts[category_name] += 1
                        if category_name not in sentiment_by_category:
                            sentiment_by_category[category_name] = []
                        sentiment_by_category[category_name].append(analysis['sentiment'])
                
            except Exception as e:
                logger.error(f"Error analyzing review {review.id}: {e}")
                continue
        
        # Get top categories
        top_categories = [cat for cat, count in category_counts.most_common(5)]
        
        # Calculate sentiment preferences
        sentiment_preferences = {}
        for category, sentiments in sentiment_by_category.items():
            positive_count = sum(1 for s in sentiments if s == 'positive')
            total_count = len(sentiments)
            sentiment_preferences[category] = positive_count / total_count if total_count > 0 else 0.5
        
        return {
            'keywords': keywords,
            'categories': top_categories,
            'sentiment_preferences': sentiment_preferences
        }
    
    def calculate_similarity_scores(self, user_preferences, products):
        """Calculate similarity scores between user preferences and products"""
        if not products.exists():
            return []
        
        # Prepare product data for vectorization
        product_texts = []
        for product in products:
            # Combine product name, description, and keywords
            text = f"{product.name} {product.description} {product.keywords}"
            product_texts.append(text)
        
        # Create TF-IDF vectors
        try:
            tfidf_matrix = self.vectorizer.fit_transform(product_texts)
        except Exception as e:
            logger.error(f"Error creating TF-IDF matrix: {e}")
            return []
        
        # Create user preference vector
        user_text = ' '.join(user_preferences['keywords'])
        user_vector = self.vectorizer.transform([user_text])
        
        # Calculate cosine similarity
        try:
            similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
        except Exception as e:
            logger.error(f"Error calculating similarities: {e}")
            return []
        
        # Create product-score pairs
        product_scores = []
        for i, product in enumerate(products):
            base_score = similarities[i] if i < len(similarities) else 0
            
            # Apply category preference boost
            category_boost = 0.2 if product.category in user_preferences['categories'] else 0
            
            # Apply sentiment preference boost
            sentiment_boost = 0
            if product.category in user_preferences['sentiment_preferences']:
                sentiment_pref = user_preferences['sentiment_preferences'][product.category]
                if sentiment_pref > 0.6:  # User likes this category
                    sentiment_boost = 0.1
            
            # Apply rating boost
            rating_boost = (product.rating - 3.0) * 0.05  # Boost for higher ratings
            
            # Calculate final score
            final_score = min(1.0, base_score + category_boost + sentiment_boost + rating_boost)
            
            product_scores.append({
                'product': product,
                'score': final_score,
                'base_score': base_score,
                'category_boost': category_boost,
                'sentiment_boost': sentiment_boost,
                'rating_boost': rating_boost
            })
        
        return product_scores
    
    def generate_recommendations(self, user, limit=5):
        """Generate product recommendations for a user"""
        try:
            # Get user preferences
            user_preferences = self.get_user_preferences(user)
            
            # Get all products
            products = Product.objects.all()
            
            if not products.exists():
                return []
            
            # Calculate similarity scores
            product_scores = self.calculate_similarity_scores(user_preferences, products)
            
            # Sort by score and get top recommendations
            product_scores.sort(key=lambda x: x['score'], reverse=True)
            top_recommendations = product_scores[:limit]
            
            # Generate reasons for recommendations
            recommendations = []
            for rec in top_recommendations:
                product = rec['product']
                score = rec['score']
                
                # Generate reason
                reasons = []
                if rec['category_boost'] > 0:
                    reasons.append(f"Based on your interest in {product.get_category_display()}")
                if rec['rating_boost'] > 0:
                    reasons.append("Highly rated by customers")
                if rec['base_score'] > 0.3:
                    reasons.append("Matches your preferences")
                
                reason = "; ".join(reasons) if reasons else "Recommended for you"
                
                # Create or update recommendation
                recommendation, created = Recommendation.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={
                        'score': score,
                        'reason': reason
                    }
                )
                
                if not created:
                    recommendation.score = score
                    recommendation.reason = reason
                    recommendation.save()
                
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user.id}: {e}")
            return []
    
    def get_recommendations_for_user(self, user, limit=5):
        """Get existing recommendations or generate new ones"""
        # Check if user has recent recommendations
        recent_recommendations = Recommendation.objects.filter(
            user=user
        ).order_by('-created_at')[:limit]
        
        # If no recent recommendations or they're old, generate new ones
        if not recent_recommendations.exists():
            return self.generate_recommendations(user, limit)
        
        # Return existing recommendations
        return list(recent_recommendations)

