from django.core.management.base import BaseCommand
from django.db import transaction
from reviews.models import Product
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with fake product data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of products to create (default: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Product data templates for more realistic products
        product_templates = [
            # Electronics
            {
                'category': 'electronics',
                'templates': [
                    {
                        'name': 'Wireless Bluetooth Headphones',
                        'description': 'High-quality wireless headphones with noise cancellation and long battery life. Perfect for music lovers and professionals.',
                        'keywords': 'wireless, bluetooth, headphones, noise cancellation, music, audio, portable',
                        'price_range': (29.99, 299.99)
                    },
                    {
                        'name': 'Smartphone',
                        'description': 'Latest smartphone with advanced camera system, fast processor, and all-day battery life.',
                        'keywords': 'smartphone, camera, mobile, phone, android, ios, battery',
                        'price_range': (199.99, 999.99)
                    },
                    {
                        'name': 'Laptop',
                        'description': 'Powerful laptop for work and entertainment with high-resolution display and fast performance.',
                        'keywords': 'laptop, computer, work, gaming, portable, performance, display',
                        'price_range': (399.99, 1999.99)
                    }
                ]
            },
            # Fashion
            {
                'category': 'fashion',
                'templates': [
                    {
                        'name': 'Casual T-Shirt',
                        'description': 'Comfortable and stylish casual t-shirt made from premium cotton. Available in various colors and sizes.',
                        'keywords': 't-shirt, casual, cotton, comfortable, fashion, clothing, style',
                        'price_range': (9.99, 49.99)
                    },
                    {
                        'name': 'Denim Jeans',
                        'description': 'Classic denim jeans with perfect fit and durability. Suitable for casual and semi-formal occasions.',
                        'keywords': 'jeans, denim, casual, fashion, clothing, durable, style',
                        'price_range': (39.99, 129.99)
                    },
                    {
                        'name': 'Running Shoes',
                        'description': 'Lightweight running shoes with excellent cushioning and support for optimal performance.',
                        'keywords': 'running, shoes, athletic, sports, comfortable, lightweight, performance',
                        'price_range': (59.99, 199.99)
                    }
                ]
            },
            # Books
            {
                'category': 'books',
                'templates': [
                    {
                        'name': 'Bestselling Novel',
                        'description': 'Award-winning novel that has captured readers worldwide with its compelling story and memorable characters.',
                        'keywords': 'book, novel, fiction, reading, literature, story, entertainment',
                        'price_range': (9.99, 29.99)
                    },
                    {
                        'name': 'Self-Help Guide',
                        'description': 'Comprehensive self-help guide with practical strategies for personal development and success.',
                        'keywords': 'self-help, personal development, motivation, success, guide, improvement',
                        'price_range': (14.99, 39.99)
                    },
                    {
                        'name': 'Cookbook',
                        'description': 'Beautiful cookbook featuring delicious recipes from around the world with stunning photography.',
                        'keywords': 'cookbook, recipes, cooking, food, kitchen, culinary, delicious',
                        'price_range': (19.99, 49.99)
                    }
                ]
            },
            # Home & Garden
            {
                'category': 'home',
                'templates': [
                    {
                        'name': 'Coffee Maker',
                        'description': 'Programmable coffee maker with built-in grinder for the perfect cup of coffee every morning.',
                        'keywords': 'coffee, maker, kitchen, appliance, morning, beverage, programmable',
                        'price_range': (49.99, 199.99)
                    },
                    {
                        'name': 'Garden Tool Set',
                        'description': 'Complete garden tool set for maintaining your outdoor space with durable, ergonomic tools.',
                        'keywords': 'garden, tools, outdoor, gardening, maintenance, durable, ergonomic',
                        'price_range': (29.99, 99.99)
                    },
                    {
                        'name': 'Throw Pillows',
                        'description': 'Decorative throw pillows to enhance your living space with comfort and style.',
                        'keywords': 'pillows, decorative, home, comfort, style, living room, decoration',
                        'price_range': (19.99, 59.99)
                    }
                ]
            },
            # Sports
            {
                'category': 'sports',
                'templates': [
                    {
                        'name': 'Yoga Mat',
                        'description': 'Premium yoga mat with excellent grip and cushioning for comfortable practice sessions.',
                        'keywords': 'yoga, mat, fitness, exercise, comfortable, grip, practice',
                        'price_range': (19.99, 79.99)
                    },
                    {
                        'name': 'Dumbbells Set',
                        'description': 'Adjustable dumbbells set for strength training and muscle building workouts.',
                        'keywords': 'dumbbells, fitness, strength, training, exercise, muscle, workout',
                        'price_range': (39.99, 199.99)
                    },
                    {
                        'name': 'Bicycle',
                        'description': 'Mountain bike perfect for outdoor adventures and daily commuting with reliable performance.',
                        'keywords': 'bicycle, bike, outdoor, adventure, commuting, mountain, cycling',
                        'price_range': (199.99, 999.99)
                    }
                ]
            }
        ]

        with transaction.atomic():
            created_count = 0
            
            for _ in range(count):
                # Select random category and template
                category_data = random.choice(product_templates)
                template = random.choice(category_data['templates'])
                
                # Generate product data
                name = template['name']
                description = template['description']
                category = category_data['category']
                keywords = template['keywords']
                price = round(random.uniform(*template['price_range']), 2)
                rating = round(random.uniform(3.0, 5.0), 1)
                
                # Generate image URL using Lorem Picsum
                image_url = f"https://picsum.photos/400/400?random={random.randint(1, 1000)}"
                
                # Create product
                product = Product.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    price=price,
                    rating=rating,
                    image_url=image_url,
                    keywords=keywords
                )
                
                created_count += 1
                
                if created_count % 10 == 0:
                    self.stdout.write(f"Created {created_count} products...")
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} products!')
            )


