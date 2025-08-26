from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reviews.models import Review, Item, Recommendation
from reviews.recommendation_engine import RecommendationEngine


class Command(BaseCommand):
    help = 'Test the recommendation system'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to test recommendations for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            return
        
        self.stdout.write(f'Testing recommendations for user: {username}')
        
        # Show user's reviews
        reviews = Review.objects.filter(user=user)
        self.stdout.write(f'\nUser has {reviews.count()} reviews:')
        for review in reviews:
            self.stdout.write(f'  - {review.category}: {review.sentiment} (score: {review.score})')
        
        # Show current recommendations
        current_recs = Recommendation.objects.filter(user=user)
        self.stdout.write(f'\nCurrent recommendations: {current_recs.count()}')
        for rec in current_recs:
            self.stdout.write(f'  - {rec.item.name} ({rec.item.category}) - Score: {rec.score}')
        
        # Generate new recommendations
        engine = RecommendationEngine()
        new_recs = engine.generate_recommendations(user, limit=5)
        
        self.stdout.write(f'\nNew recommendations generated: {len(new_recs)}')
        for rec in new_recs:
            self.stdout.write(f'  - {rec.item.name} ({rec.item.category}) - Score: {rec.score}')
            self.stdout.write(f'    Reason: {rec.reason}')
        
        self.stdout.write(self.style.SUCCESS('\nRecommendation test completed!'))
