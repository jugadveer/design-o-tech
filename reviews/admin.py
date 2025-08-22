from django.contrib import admin
from .models import Review, AnalysisResult, Product, Recommendation


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "short_text")
    search_fields = ("raw_text",)

    def short_text(self, obj):
        return obj.raw_text[:60]


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ("review", "sentiment", "emotion", "polarity", "subjectivity", "created_at")
    list_filter = ("sentiment", "emotion")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "rating", "created_at")
    list_filter = ("category", "rating")
    search_fields = ("name", "description")


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "score", "reason", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("user__username", "product__name", "reason")

# Register your models here.
