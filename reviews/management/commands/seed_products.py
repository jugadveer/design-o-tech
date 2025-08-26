from django.core.management.base import BaseCommand
from reviews.models import Item


class Command(BaseCommand):
    help = 'Seed the database with sample items'

    def handle(self, *args, **options):
        products_data = [
            # Electronics (10 products)
            {
                'name': 'iPhone 15 Pro',
                'description': 'Latest iPhone with advanced camera system and A17 Pro chip',
                'category': 'electronics',
                'price': 999.99,
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop',
                'keywords': 'smartphone, camera, apple, ios, premium'
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Android flagship with AI features and excellent performance',
                'category': 'electronics',
                'price': 899.99,
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
                'keywords': 'android, smartphone, samsung, ai, camera'
            },
            {
                'name': 'MacBook Pro 14"',
                'description': 'Professional laptop with M3 chip and Retina display',
                'category': 'electronics',
                'price': 1999.99,
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop',
                'keywords': 'laptop, macbook, apple, professional, m3'
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Premium noise-cancelling wireless headphones',
                'category': 'electronics',
                'price': 399.99,
                'rating': 4.7,
                'keywords': 'headphones, sony, noise-cancelling, wireless, premium'
            },
            {
                'name': 'iPad Air 5th Gen',
                'description': 'Versatile tablet with M1 chip and Apple Pencil support',
                'category': 'electronics',
                'price': 599.99,
                'rating': 4.6,
                'keywords': 'tablet, ipad, apple, m1, pencil'
            },
            {
                'name': 'Dell XPS 13',
                'description': 'Ultra-thin laptop with InfinityEdge display',
                'category': 'electronics',
                'price': 1299.99,
                'rating': 4.5,
                'keywords': 'laptop, dell, xps, thin, premium'
            },
            {
                'name': 'GoPro Hero 11',
                'description': 'Action camera with 5.3K video and HyperSmooth stabilization',
                'category': 'electronics',
                'price': 399.99,
                'rating': 4.4,
                'keywords': 'camera, gopro, action, video, stabilization'
            },
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Gaming console with 7-inch OLED screen',
                'category': 'electronics',
                'price': 349.99,
                'rating': 4.7,
                'keywords': 'gaming, nintendo, switch, oled, portable'
            },
            {
                'name': 'Samsung 65" QLED TV',
                'description': '4K QLED smart TV with Quantum HDR',
                'category': 'electronics',
                'price': 1299.99,
                'rating': 4.6,
                'keywords': 'tv, samsung, qled, 4k, smart'
            },
            {
                'name': 'AirPods Pro 2nd Gen',
                'description': 'Wireless earbuds with active noise cancellation',
                'category': 'electronics',
                'price': 249.99,
                'rating': 4.5,
                'keywords': 'earbuds, apple, wireless, noise-cancelling, premium'
            },
            
            # Fashion (10 products)
            {
                'name': 'Nike Air Max 270',
                'description': 'Comfortable running shoes with Air Max technology',
                'category': 'fashion',
                'price': 150.00,
                'rating': 4.5,
                'keywords': 'shoes, running, nike, comfortable, athletic'
            },
            {
                'name': 'Adidas Ultraboost 22',
                'description': 'Premium running shoes with responsive cushioning',
                'category': 'fashion',
                'price': 180.00,
                'rating': 4.7,
                'keywords': 'running, shoes, adidas, boost, performance'
            },
            {
                'name': 'Levi\'s 501 Original Jeans',
                'description': 'Classic straight-fit jeans with authentic styling',
                'category': 'fashion',
                'price': 89.99,
                'rating': 4.4,
                'keywords': 'jeans, levis, classic, denim, straight-fit'
            },
            {
                'name': 'Ray-Ban Aviator Classic',
                'description': 'Timeless aviator sunglasses with UV protection',
                'category': 'fashion',
                'price': 154.99,
                'rating': 4.6,
                'keywords': 'sunglasses, ray-ban, aviator, classic, uv'
            },
            {
                'name': 'Michael Kors Tote Bag',
                'description': 'Elegant leather tote bag with gold hardware',
                'category': 'fashion',
                'price': 299.99,
                'rating': 4.3,
                'keywords': 'bag, michael kors, leather, tote, elegant'
            },
            {
                'name': 'Calvin Klein Underwear Set',
                'description': 'Comfortable cotton underwear set for everyday wear',
                'category': 'fashion',
                'price': 45.99,
                'rating': 4.2,
                'keywords': 'underwear, calvin klein, cotton, comfortable, set'
            },
            {
                'name': 'Converse Chuck Taylor All Star',
                'description': 'Iconic canvas sneakers with rubber toe cap',
                'category': 'fashion',
                'price': 65.00,
                'rating': 4.5,
                'keywords': 'sneakers, converse, canvas, classic, iconic'
            },
            {
                'name': 'Fossil Watch Classic',
                'description': 'Analog watch with leather strap and minimalist design',
                'category': 'fashion',
                'price': 129.99,
                'rating': 4.4,
                'keywords': 'watch, fossil, analog, leather, classic'
            },
            {
                'name': 'Zara Blazer Jacket',
                'description': 'Modern blazer jacket perfect for office wear',
                'category': 'fashion',
                'price': 89.99,
                'rating': 4.1,
                'keywords': 'blazer, zara, jacket, office, modern'
            },
            {
                'name': 'H&M Summer Dress',
                'description': 'Floral print summer dress with adjustable straps',
                'category': 'fashion',
                'price': 39.99,
                'rating': 4.0,
                'keywords': 'dress, h&m, summer, floral, casual'
            },
            
            # Books (10 products)
            {
                'name': 'The Great Gatsby',
                'description': 'Classic American novel by F. Scott Fitzgerald',
                'category': 'books',
                'price': 12.99,
                'rating': 4.9,
                'keywords': 'classic, literature, american, fiction, jazz age'
            },
            {
                'name': 'To Kill a Mockingbird',
                'description': 'Harper Lee\'s masterpiece about justice and racism',
                'category': 'books',
                'price': 14.99,
                'rating': 4.8,
                'keywords': 'classic, literature, american, justice, coming of age'
            },
            {
                'name': '1984 by George Orwell',
                'description': 'Dystopian novel about totalitarianism and surveillance',
                'category': 'books',
                'price': 11.99,
                'rating': 4.7,
                'keywords': 'dystopian, orwell, classic, political, fiction'
            },
            {
                'name': 'The Hobbit',
                'description': 'J.R.R. Tolkien\'s fantasy adventure novel',
                'category': 'books',
                'price': 15.99,
                'rating': 4.8,
                'keywords': 'fantasy, tolkien, adventure, hobbit, middle-earth'
            },
            {
                'name': 'Pride and Prejudice',
                'description': 'Jane Austen\'s romantic comedy of manners',
                'category': 'books',
                'price': 9.99,
                'rating': 4.6,
                'keywords': 'romance, austen, classic, english, manners'
            },
            {
                'name': 'The Catcher in the Rye',
                'description': 'J.D. Salinger\'s coming-of-age novel',
                'category': 'books',
                'price': 13.99,
                'rating': 4.5,
                'keywords': 'coming-of-age, salinger, american, classic, youth'
            },
            {
                'name': 'Lord of the Flies',
                'description': 'William Golding\'s allegorical novel about human nature',
                'category': 'books',
                'price': 10.99,
                'rating': 4.4,
                'keywords': 'allegory, golding, human nature, survival, classic'
            },
            {
                'name': 'The Alchemist',
                'description': 'Paulo Coelho\'s inspirational novel about destiny',
                'category': 'books',
                'price': 16.99,
                'rating': 4.3,
                'keywords': 'inspirational, coelho, destiny, journey, fiction'
            },
            {
                'name': 'Animal Farm',
                'description': 'George Orwell\'s political allegory about revolution',
                'category': 'books',
                'price': 8.99,
                'rating': 4.6,
                'keywords': 'allegory, orwell, political, revolution, satire'
            },
            {
                'name': 'The Little Prince',
                'description': 'Antoine de Saint-Exupéry\'s philosophical children\'s book',
                'category': 'books',
                'price': 7.99,
                'rating': 4.7,
                'keywords': 'philosophy, children, saint-exupéry, classic, wisdom'
            },
            
            # Home (10 products)
            {
                'name': 'IKEA MALM Bed Frame',
                'description': 'Modern bed frame with storage drawers',
                'category': 'home',
                'price': 299.99,
                'rating': 4.3,
                'keywords': 'bed, furniture, ikea, storage, modern'
            },
            {
                'name': 'Philips Hue Smart Bulb',
                'description': 'Smart LED bulb with color control and voice assistant support',
                'category': 'home',
                'price': 49.99,
                'rating': 4.4,
                'keywords': 'smart home, led, philips, voice control, lighting'
            },
            {
                'name': 'Dyson V15 Detect',
                'description': 'Cordless vacuum with laser dust detection',
                'category': 'home',
                'price': 699.99,
                'rating': 4.8,
                'keywords': 'vacuum, dyson, cordless, laser, cleaning'
            },
            {
                'name': 'KitchenAid Stand Mixer',
                'description': 'Professional stand mixer for baking and cooking',
                'category': 'home',
                'price': 399.99,
                'rating': 4.7,
                'keywords': 'mixer, kitchenaid, baking, cooking, professional'
            },
            {
                'name': 'Nest Learning Thermostat',
                'description': 'Smart thermostat that learns your preferences',
                'category': 'home',
                'price': 249.99,
                'rating': 4.5,
                'keywords': 'thermostat, nest, smart, learning, energy'
            },
            {
                'name': 'West Elm Sofa',
                'description': 'Modern sectional sofa with premium fabric',
                'category': 'home',
                'price': 1299.99,
                'rating': 4.2,
                'keywords': 'sofa, west elm, modern, sectional, premium'
            },
            {
                'name': 'Cuisinart Coffee Maker',
                'description': 'Programmable coffee maker with thermal carafe',
                'category': 'home',
                'price': 89.99,
                'rating': 4.3,
                'keywords': 'coffee maker, cuisinart, programmable, thermal'
            },
            {
                'name': 'Ring Video Doorbell',
                'description': 'Smart video doorbell with motion detection',
                'category': 'home',
                'price': 199.99,
                'rating': 4.4,
                'keywords': 'doorbell, ring, smart, video, security'
            },
            {
                'name': 'Crate & Barrel Dinnerware Set',
                'description': 'Elegant porcelain dinnerware set for 8',
                'category': 'home',
                'price': 199.99,
                'rating': 4.1,
                'keywords': 'dinnerware, crate & barrel, porcelain, elegant, set'
            },
            {
                'name': 'Bissell Carpet Cleaner',
                'description': 'Professional carpet cleaner for deep cleaning',
                'category': 'home',
                'price': 299.99,
                'rating': 4.0,
                'keywords': 'carpet cleaner, bissell, professional, deep cleaning'
            },
            
            # Sports (10 products)
            {
                'name': 'Wilson Tennis Racket',
                'description': 'Professional tennis racket for advanced players',
                'category': 'sports',
                'price': 199.99,
                'rating': 4.6,
                'keywords': 'tennis, racket, wilson, professional, sports'
            },
            {
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip yoga mat with alignment lines',
                'category': 'sports',
                'price': 39.99,
                'rating': 4.5,
                'keywords': 'yoga, mat, exercise, fitness, non-slip'
            },
            {
                'name': 'Nike Basketball Shoes',
                'description': 'High-performance basketball shoes with ankle support',
                'category': 'sports',
                'price': 129.99,
                'rating': 4.4,
                'keywords': 'basketball, nike, shoes, performance, ankle support'
            },
            {
                'name': 'Fitbit Charge 5',
                'description': 'Advanced fitness tracker with GPS and heart rate',
                'category': 'sports',
                'price': 179.99,
                'rating': 4.3,
                'keywords': 'fitness tracker, fitbit, gps, heart rate, health'
            },
            {
                'name': 'Under Armour Compression Shirt',
                'description': 'Moisture-wicking compression shirt for workouts',
                'category': 'sports',
                'price': 34.99,
                'rating': 4.2,
                'keywords': 'compression, under armour, moisture-wicking, workout'
            },
            {
                'name': 'Adidas Soccer Ball',
                'description': 'Professional soccer ball with FIFA quality mark',
                'category': 'sports',
                'price': 89.99,
                'rating': 4.5,
                'keywords': 'soccer, adidas, ball, professional, fifa'
            },
            {
                'name': 'Bowflex SelectTech Dumbbells',
                'description': 'Adjustable dumbbells with weight selection dial',
                'category': 'sports',
                'price': 399.99,
                'rating': 4.7,
                'keywords': 'dumbbells, bowflex, adjustable, weight, fitness'
            },
            {
                'name': 'Garmin Forerunner 245',
                'description': 'GPS running watch with advanced training metrics',
                'category': 'sports',
                'price': 299.99,
                'rating': 4.6,
                'keywords': 'gps watch, garmin, running, training, metrics'
            },
            {
                'name': 'Lululemon Leggings',
                'description': 'High-performance yoga leggings with four-way stretch',
                'category': 'sports',
                'price': 98.00,
                'rating': 4.4,
                'keywords': 'leggings, lululemon, yoga, performance, stretch'
            },
            {
                'name': 'Yeti Rambler Water Bottle',
                'description': 'Insulated water bottle that keeps drinks cold for hours',
                'category': 'sports',
                'price': 39.99,
                'rating': 4.8,
                'keywords': 'water bottle, yeti, insulated, cold, durable'
            },
            
            # Beauty (10 products)
            {
                'name': 'L\'Oreal Paris Foundation',
                'description': 'Long-lasting foundation with natural finish',
                'category': 'beauty',
                'price': 24.99,
                'rating': 4.2,
                'keywords': 'makeup, foundation, loreal, beauty, long-lasting'
            },
            {
                'name': 'Dove Body Wash',
                'description': 'Moisturizing body wash for sensitive skin',
                'category': 'beauty',
                'price': 8.99,
                'rating': 4.4,
                'keywords': 'body wash, dove, moisturizing, sensitive skin, bath'
            },
            {
                'name': 'MAC Lipstick Ruby Woo',
                'description': 'Iconic matte red lipstick with long-lasting color',
                'category': 'beauty',
                'price': 19.99,
                'rating': 4.6,
                'keywords': 'lipstick, mac, matte, red, long-lasting'
            },
            {
                'name': 'Neutrogena Face Wash',
                'description': 'Gentle facial cleanser for all skin types',
                'category': 'beauty',
                'price': 12.99,
                'rating': 4.3,
                'keywords': 'face wash, neutrogena, gentle, cleanser, skincare'
            },
            {
                'name': 'Maybelline Mascara',
                'description': 'Volumizing mascara with curved brush',
                'category': 'beauty',
                'price': 9.99,
                'rating': 4.1,
                'keywords': 'mascara, maybelline, volumizing, curved brush, makeup'
            },
            {
                'name': 'Cetaphil Moisturizer',
                'description': 'Fragrance-free moisturizer for sensitive skin',
                'category': 'beauty',
                'price': 15.99,
                'rating': 4.5,
                'keywords': 'moisturizer, cetaphil, fragrance-free, sensitive, skincare'
            },
            {
                'name': 'Revlon Hair Dryer',
                'description': 'Professional hair dryer with ionic technology',
                'category': 'beauty',
                'price': 39.99,
                'rating': 4.2,
                'keywords': 'hair dryer, revlon, professional, ionic, styling'
            },
            {
                'name': 'Burt\'s Bees Lip Balm',
                'description': 'Natural lip balm with beeswax and vitamin E',
                'category': 'beauty',
                'price': 3.99,
                'rating': 4.4,
                'keywords': 'lip balm, burts bees, natural, beeswax, moisturizing'
            },
            {
                'name': 'CoverGirl Concealer',
                'description': 'Full-coverage concealer for dark circles and blemishes',
                'category': 'beauty',
                'price': 8.99,
                'rating': 4.0,
                'keywords': 'concealer, covergirl, full-coverage, dark circles, makeup'
            },
            {
                'name': 'Aveeno Body Lotion',
                'description': 'Daily moisturizing lotion with colloidal oatmeal',
                'category': 'beauty',
                'price': 11.99,
                'rating': 4.3,
                'keywords': 'body lotion, aveeno, moisturizing, oatmeal, daily'
            },
            
            # Toys (10 products)
            {
                'name': 'LEGO Star Wars Set',
                'description': 'Collector\'s edition Star Wars LEGO set',
                'category': 'toys',
                'price': 79.99,
                'rating': 4.8,
                'keywords': 'lego, star wars, collector, building, toys'
            },
            {
                'name': 'Nintendo Switch',
                'description': 'Hybrid gaming console for home and portable play',
                'category': 'toys',
                'price': 299.99,
                'rating': 4.7,
                'keywords': 'gaming, nintendo, switch, portable, console'
            },
            {
                'name': 'Barbie Dreamhouse',
                'description': 'Three-story dollhouse with furniture and accessories',
                'category': 'toys',
                'price': 199.99,
                'rating': 4.5,
                'keywords': 'barbie, dollhouse, dreamhouse, furniture, dolls'
            },
            {
                'name': 'Hot Wheels Track Set',
                'description': 'Ultimate racing track with multiple cars and loops',
                'category': 'toys',
                'price': 49.99,
                'rating': 4.3,
                'keywords': 'hot wheels, track, racing, cars, loops'
            },
            {
                'name': 'PlayStation 5',
                'description': 'Next-generation gaming console with 4K graphics',
                'category': 'toys',
                'price': 499.99,
                'rating': 4.9,
                'keywords': 'gaming, playstation, ps5, 4k, console'
            },
            {
                'name': 'Fisher-Price Activity Center',
                'description': 'Interactive activity center for babies and toddlers',
                'category': 'toys',
                'price': 69.99,
                'rating': 4.2,
                'keywords': 'fisher-price, activity center, baby, toddler, interactive'
            },
            {
                'name': 'Monopoly Board Game',
                'description': 'Classic property trading board game for family fun',
                'category': 'toys',
                'price': 24.99,
                'rating': 4.4,
                'keywords': 'monopoly, board game, classic, family, property'
            },
            {
                'name': 'Nerf Blaster Set',
                'description': 'Foam dart blaster set with multiple accessories',
                'category': 'toys',
                'price': 34.99,
                'rating': 4.1,
                'keywords': 'nerf, blaster, foam darts, accessories, action'
            },
            {
                'name': 'Crayola Art Set',
                'description': 'Complete art set with markers, crayons, and paper',
                'category': 'toys',
                'price': 19.99,
                'rating': 4.6,
                'keywords': 'crayola, art set, markers, crayons, creative'
            },
            {
                'name': 'Remote Control Car',
                'description': 'High-speed RC car with rechargeable battery',
                'category': 'toys',
                'price': 89.99,
                'rating': 4.3,
                'keywords': 'rc car, remote control, high-speed, rechargeable, action'
            },
            
            # Automotive (10 products)
            {
                'name': 'Car Air Freshener',
                'description': 'Long-lasting car air freshener with natural scent',
                'category': 'automotive',
                'price': 12.99,
                'rating': 4.1,
                'keywords': 'car, air freshener, scent, automotive, interior'
            },
            {
                'name': 'Dash Cam HD',
                'description': 'High-definition dashboard camera with night vision',
                'category': 'automotive',
                'price': 89.99,
                'rating': 4.3,
                'keywords': 'dash cam, camera, automotive, recording, safety'
            },
            {
                'name': 'Car Phone Mount',
                'description': 'Universal phone holder for car dashboard',
                'category': 'automotive',
                'price': 19.99,
                'rating': 4.2,
                'keywords': 'phone mount, car, universal, dashboard, holder'
            },
            {
                'name': 'Jump Starter Portable',
                'description': 'Portable car battery jump starter with USB ports',
                'category': 'automotive',
                'price': 79.99,
                'rating': 4.5,
                'keywords': 'jump starter, portable, battery, car, emergency'
            },
            {
                'name': 'Car Floor Mats',
                'description': 'All-weather car floor mats with custom fit',
                'category': 'automotive',
                'price': 45.99,
                'rating': 4.0,
                'keywords': 'floor mats, car, all-weather, custom fit, protection'
            },
            {
                'name': 'Bluetooth Car Adapter',
                'description': 'Wireless Bluetooth adapter for car audio system',
                'category': 'automotive',
                'price': 29.99,
                'rating': 4.1,
                'keywords': 'bluetooth, adapter, car, audio, wireless'
            },
            {
                'name': 'Car Wash Kit',
                'description': 'Complete car washing kit with microfiber towels',
                'category': 'automotive',
                'price': 39.99,
                'rating': 4.3,
                'keywords': 'car wash, kit, microfiber, cleaning, complete'
            },
            {
                'name': 'Tire Pressure Gauge',
                'description': 'Digital tire pressure gauge with backlight',
                'category': 'automotive',
                'price': 15.99,
                'rating': 4.4,
                'keywords': 'tire pressure, gauge, digital, backlight, automotive'
            },
            {
                'name': 'Car Seat Covers',
                'description': 'Universal car seat covers with easy installation',
                'category': 'automotive',
                'price': 59.99,
                'rating': 4.0,
                'keywords': 'seat covers, car, universal, protection, installation'
            },
            {
                'name': 'Emergency Car Kit',
                'description': 'Complete emergency kit with first aid and tools',
                'category': 'automotive',
                'price': 89.99,
                'rating': 4.6,
                'keywords': 'emergency kit, car, first aid, tools, safety'
            },
            
            # Health (10 products)
            {
                'name': 'Vitamin D3 Supplements',
                'description': 'High-potency vitamin D3 for bone health',
                'category': 'health',
                'price': 19.99,
                'rating': 4.5,
                'keywords': 'vitamins, health, supplements, d3, bone health'
            },
            {
                'name': 'Fitness Tracker',
                'description': 'Smart fitness tracker with heart rate monitoring',
                'category': 'health',
                'price': 149.99,
                'rating': 4.4,
                'keywords': 'fitness, tracker, health, monitoring, smart'
            },
            {
                'name': 'Yoga Block Set',
                'description': 'High-density foam yoga blocks for support',
                'category': 'health',
                'price': 24.99,
                'rating': 4.3,
                'keywords': 'yoga blocks, foam, support, exercise, fitness'
            },
            {
                'name': 'Protein Powder',
                'description': 'Whey protein powder for muscle building and recovery',
                'category': 'health',
                'price': 49.99,
                'rating': 4.6,
                'keywords': 'protein powder, whey, muscle, recovery, fitness'
            },
            {
                'name': 'Blood Pressure Monitor',
                'description': 'Digital blood pressure monitor for home use',
                'category': 'health',
                'price': 39.99,
                'rating': 4.2,
                'keywords': 'blood pressure, monitor, digital, home, health'
            },
            {
                'name': 'Resistance Bands Set',
                'description': 'Multi-level resistance bands for strength training',
                'category': 'health',
                'price': 19.99,
                'rating': 4.4,
                'keywords': 'resistance bands, strength training, fitness, exercise'
            },
            {
                'name': 'Essential Oil Diffuser',
                'description': 'Ultrasonic essential oil diffuser with LED lights',
                'category': 'health',
                'price': 34.99,
                'rating': 4.1,
                'keywords': 'essential oils, diffuser, ultrasonic, aromatherapy, wellness'
            },
            {
                'name': 'Digital Scale',
                'description': 'Precision digital bathroom scale with body composition',
                'category': 'health',
                'price': 29.99,
                'rating': 4.3,
                'keywords': 'digital scale, bathroom, precision, body composition, health'
            },
            {
                'name': 'Foam Roller',
                'description': 'High-density foam roller for muscle recovery',
                'category': 'health',
                'price': 22.99,
                'rating': 4.5,
                'keywords': 'foam roller, muscle recovery, massage, fitness, therapy'
            },
            {
                'name': 'Sleep Mask',
                'description': 'Silk sleep mask for better sleep quality',
                'category': 'health',
                'price': 18.99,
                'rating': 4.0,
                'keywords': 'sleep mask, silk, sleep quality, comfort, wellness'
            },
            
            # Food (10 products)
            {
                'name': 'Organic Coffee Beans',
                'description': 'Premium organic coffee beans from single origin',
                'category': 'food',
                'price': 24.99,
                'rating': 4.6,
                'keywords': 'coffee, organic, beans, premium, single origin'
            },
            {
                'name': 'Dark Chocolate Bar',
                'description': '70% dark chocolate with sea salt',
                'category': 'food',
                'price': 6.99,
                'rating': 4.3,
                'keywords': 'chocolate, dark, organic, sea salt, premium'
            },
            {
                'name': 'Quinoa Organic',
                'description': 'Premium organic quinoa for healthy meals',
                'category': 'food',
                'price': 12.99,
                'rating': 4.4,
                'keywords': 'quinoa, organic, healthy, grains, premium'
            },
            {
                'name': 'Extra Virgin Olive Oil',
                'description': 'Cold-pressed extra virgin olive oil from Italy',
                'category': 'food',
                'price': 18.99,
                'rating': 4.7,
                'keywords': 'olive oil, extra virgin, cold-pressed, italy, premium'
            },
            {
                'name': 'Almond Butter Natural',
                'description': 'Natural almond butter without added sugar',
                'category': 'food',
                'price': 14.99,
                'rating': 4.2,
                'keywords': 'almond butter, natural, no sugar, healthy, spread'
            },
            {
                'name': 'Green Tea Bags',
                'description': 'Premium green tea bags with antioxidants',
                'category': 'food',
                'price': 8.99,
                'rating': 4.5,
                'keywords': 'green tea, antioxidants, premium, healthy, natural'
            },
            {
                'name': 'Honey Raw Organic',
                'description': 'Pure raw organic honey from local beekeepers',
                'category': 'food',
                'price': 16.99,
                'rating': 4.6,
                'keywords': 'honey, raw, organic, local, pure'
            },
            {
                'name': 'Mixed Nuts Premium',
                'description': 'Premium mixed nuts with no added salt',
                'category': 'food',
                'price': 22.99,
                'rating': 4.3,
                'keywords': 'mixed nuts, premium, no salt, healthy, snack'
            },
            {
                'name': 'Coconut Oil Virgin',
                'description': 'Cold-pressed virgin coconut oil for cooking',
                'category': 'food',
                'price': 11.99,
                'rating': 4.4,
                'keywords': 'coconut oil, virgin, cold-pressed, cooking, natural'
            },
            {
                'name': 'Dried Cranberries',
                'description': 'Sweetened dried cranberries for snacking',
                'category': 'food',
                'price': 9.99,
                'rating': 4.1,
                'keywords': 'dried cranberries, sweetened, snack, healthy, natural'
            }
        ]

        created_count = 0
        for item_data in products_data:
            item, created = Item.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created item: {item.name}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} items')
        )


