from django.urls import path
from . import views

urlpatterns = [
    # API endpoints only - main routes are handled in smart_analyzer/urls.py
    path('api/sentiment/', views.analyze_sentiment, name='analyze_sentiment'),
    path('api/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('api/recommendations/refresh/', views.refresh_recommendations, name='refresh_recommendations'),
]


