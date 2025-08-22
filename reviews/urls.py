from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('input/', views.review_input, name='review_input'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api/sentiment/', views.analyze_sentiment, name='analyze_sentiment'),
    path('api/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('api/recommendations/refresh/', views.refresh_recommendations, name='refresh_recommendations'),
]


