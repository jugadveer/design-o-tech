from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion & Apparel'),
        ('books', 'Books & Media'),
        ('home', 'Home & Garden'),
        ('sports', 'Sports & Outdoors'),
        ('beauty', 'Beauty & Personal Care'),
        ('toys', 'Toys & Games'),
        ('automotive', 'Automotive'),
        ('health', 'Health & Wellness'),
        ('food', 'Food & Beverages'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    image_url = models.URLField(max_length=500, blank=True)
    keywords = models.TextField(blank=True, help_text="Comma-separated keywords for recommendation matching")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_keywords_list(self):
        if self.keywords:
            return [kw.strip().lower() for kw in self.keywords.split(',')]
        return []


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50, choices=Item.CATEGORY_CHOICES, null=True, blank=True)
    raw_text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.raw_text[:50]


class AnalysisResult(models.Model):
    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
        ("neutral", "Neutral"),
    ]

    EMOTION_CHOICES = [
        ("happy", "Happy"),
        ("angry", "Angry"),
        ("sad", "Sad"),
        ("surprised", "Surprised"),
        ("neutral", "Neutral"),
    ]

    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name="analysis")
    sentiment = models.CharField(max_length=16, choices=SENTIMENT_CHOICES)
    polarity = models.FloatField(default=0.0)
    subjectivity = models.FloatField(default=0.0)
    emotion = models.CharField(max_length=16, choices=EMOTION_CHOICES, default="neutral")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.review_id} - {self.sentiment}/{self.emotion}"


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0, help_text="Recommendation score (0-1)")
    reason = models.CharField(max_length=200, blank=True, help_text="Why this item was recommended")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'item']
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.item.name} (Score: {self.score:.2f})"
