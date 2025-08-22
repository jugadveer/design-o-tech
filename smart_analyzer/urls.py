"""
URL configuration for smart_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reviews import views as review_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', review_views.landing, name='home'),
    path('about/', review_views.about, name='about'),
    path('dashboard/', review_views.dashboard, name='dashboard'),
    path('input/', review_views.review_input, name='review_input'),
    path('login/', auth_views.LoginView.as_view(next_page='dashboard'), name='login'),
    path('logout/', review_views.logout_view, name='logout'),
    path('analyze-sentiment/', review_views.analyze_sentiment, name='analyze_sentiment'),
    path('signup/', review_views.signup, name='signup'),
    
    # Recommendation API endpoints
    path('api/recommendations/', review_views.get_recommendations, name='get_recommendations'),
    path('api/recommendations/refresh/', review_views.refresh_recommendations, name='refresh_recommendations'),
]
