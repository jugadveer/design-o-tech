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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reviews import views as review_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', review_views.landing, name='home'),
    path('about/', review_views.about, name='about'),
    path('dashboard/', review_views.dashboard, name='dashboard'),
    path('input/', review_views.review_input, name='review_input'),
    path('profile/', review_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(next_page='dashboard'), name='login'),
    path('logout/', review_views.logout_view, name='logout'),
    path('signup/', review_views.signup, name='signup'),
    
    # API endpoints
    path('api/sentiment/', review_views.analyze_sentiment, name='analyze_sentiment'),
    path('api/recommendations/', review_views.get_recommendations, name='get_recommendations'),
    path('api/recommendations/refresh/', review_views.refresh_recommendations, name='refresh_recommendations'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serve static files in production
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
