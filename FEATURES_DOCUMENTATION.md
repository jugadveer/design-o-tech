# Review Analyzer - Smart Review Analysis & Recommendation System

## 🎯 Project Overview

**Review Analyzer** is an intelligent web application that combines Natural Language Processing (NLP) with machine learning to analyze user reviews and provide personalized product recommendations. Built with Django, it offers sentiment analysis, emotion detection, and a sophisticated recommendation engine.

## 🚀 Core Features

### 1. **Sentiment Analysis Engine**
- **Technology**: TextBlob + Custom Heuristics
- **Capabilities**:
  - Polarity scoring (-1 to +1 scale)
  - Subjectivity analysis (0 to 1 scale)
  - Sentiment classification (Positive/Negative/Neutral)
  - Custom pattern recognition for common phrases
  - Negation handling ("didn't like", "not good", etc.)

**How it works**:
```python
# Analyzes text using TextBlob + custom patterns
result = analyze_text("This product is amazing!")
# Returns: {"sentiment": "positive", "polarity": 0.8, "subjectivity": 0.6}
```

### 2. **Emotion Detection System**
- **Supported Emotions**: Happy, Angry, Sad, Surprised, Neutral
- **Keyword-based detection** with emotion-specific vocabulary
- **Real-time analysis** during review submission

**Emotion Keywords**:
- Happy: "happy", "joy", "delight", "love", "great", "awesome"
- Angry: "angry", "hate", "rage", "furious", "worst", "terrible"
- Sad: "sad", "unhappy", "disappointed", "depress"
- Surprised: "surprised", "amazed", "shocked", "wow"

### 3. **Intelligent Recommendation Engine**
- **Multi-factor scoring system**:
  - User preference analysis based on review history
  - Category affinity scoring
  - Product rating integration
  - Diversity balancing (liked categories + discovery items)

**Recommendation Algorithm**:
```python
# User preference analysis
liked_categories = analyze_user_sentiment_by_category()
# Score calculation
base_score = item.rating / 5.0
category_boost = 0.1 if item.category in liked_categories else 0
final_score = min(1.0, base_score + category_boost)
```

### 4. **Review Input System**
- **Multiple input methods**:
  - Direct text input
  - File upload (.txt files)
  - Batch processing (multiple reviews at once)
- **Automatic text chunking** for large inputs
- **Real-time sentiment preview**

### 5. **Interactive Dashboard**
- **Key Metrics Display**:
  - Total reviews count
  - Sentiment distribution (Positive/Negative/Neutral percentages)
  - Average polarity score
  - Category-wise statistics
- **Visual Analytics**:
  - Sentiment distribution charts
  - Word frequency analysis
  - Word cloud generation
- **Personalized Recommendations**:
  - Top 5 recommended products
  - Recommendation reasoning
  - Product images and details

### 6. **User Profile & Analytics**
- **Review History**: Complete timeline of all user reviews
- **Category Performance**: Sentiment analysis by product category
- **Recommendation History**: Past recommendations with scores
- **Personal Statistics**: Review patterns and preferences

### 7. **Product Database**
- **100+ Curated Products** across 10 categories:
  - Electronics (iPhone, MacBook, etc.)
  - Fashion & Apparel (Nike, Adidas, etc.)
  - Books & Media (Classic literature)
  - Home & Garden (IKEA, Dyson, etc.)
  - Sports & Outdoors (Fitness equipment)
  - Beauty & Personal Care (Cosmetics, skincare)
  - Toys & Games (LEGO, Nintendo, etc.)
  - Automotive (Car accessories)
  - Health & Wellness (Supplements, fitness)
  - Food & Beverages (Organic products)

## 🔧 Technical Architecture

### **Backend Stack**
- **Framework**: Django 5.2.5
- **Database**: SQLite (production-ready for PostgreSQL)
- **NLP Libraries**: TextBlob, NLTK, WordCloud
- **ML Libraries**: scikit-learn, NumPy, SciPy
- **Deployment**: Gunicorn + WhiteNoise

### **Frontend Technologies**
- **UI Framework**: Bootstrap 5.3.3
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6.5.0
- **Typography**: Inter font family
- **Responsive Design**: Mobile-first approach

### **Data Models**

#### **Item Model**
```python
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    image_url = models.URLField(max_length=500)
    keywords = models.TextField(help_text="Comma-separated keywords")
```

#### **Review Model**
```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=Item.CATEGORY_CHOICES)
    raw_text = models.TextField()
    sentiment = models.CharField(max_length=20)
    score = models.FloatField(default=0.0)
```

#### **AnalysisResult Model**
```python
class AnalysisResult(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=16, choices=SENTIMENT_CHOICES)
    polarity = models.FloatField(default=0.0)
    subjectivity = models.FloatField(default=0.0)
    emotion = models.CharField(max_length=16, choices=EMOTION_CHOICES)
```

#### **Recommendation Model**
```python
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    reason = models.CharField(max_length=200)
```

## 🌐 API Endpoints

### **Authentication Endpoints**
- `POST /signup/` - User registration
- `GET /login/` - User login
- `GET /logout/` - User logout

### **Core Functionality Endpoints**
- `GET /` - Landing page
- `GET /dashboard/` - Main dashboard (requires login)
- `GET /profile/` - User profile (requires login)
- `GET /input/` - Review input form (requires login)
- `GET /about/` - About page

### **API Endpoints**
- `POST /api/sentiment/` - Real-time sentiment analysis
- `GET /api/recommendations/` - Get user recommendations
- `POST /api/recommendations/refresh/` - Force refresh recommendations

## 📊 Data Flow & Processing

### **Review Processing Pipeline**
1. **Input Reception**: User submits review text/file
2. **Text Chunking**: Automatic splitting of large inputs
3. **Sentiment Analysis**: TextBlob + custom heuristics
4. **Emotion Detection**: Keyword-based emotion classification
5. **Database Storage**: Bulk creation of reviews and analysis results
6. **Recommendation Update**: Automatic refresh of user recommendations
7. **Word Cloud Generation**: Asynchronous word cloud creation

### **Recommendation Generation Process**
1. **User Preference Analysis**: Analyze review history by category
2. **Sentiment Scoring**: Calculate category affinity based on positive reviews
3. **Product Filtering**: Select items with ratings ≥ 3.5
4. **Diversity Balancing**: Mix liked categories with discovery items
5. **Score Calculation**: Combine rating, category preference, and diversity
6. **Reasoning Generation**: Create human-readable recommendation explanations

## 🎨 User Experience Features

### **Modern UI/UX Design**
- **Clean, minimalist interface** with modern color scheme
- **Responsive design** that works on all devices
- **Smooth animations** and hover effects
- **Intuitive navigation** with clear visual hierarchy
- **Loading states** and progress indicators

### **Interactive Elements**
- **Real-time sentiment preview** during review input
- **Dynamic charts** that update with new data
- **Hover tooltips** for detailed information
- **Smooth transitions** between pages
- **Auto-refresh** recommendations after new reviews

### **Accessibility Features**
- **Semantic HTML** structure
- **Keyboard navigation** support
- **Screen reader** compatibility
- **High contrast** color scheme
- **Responsive typography**

## 🔒 Security & Performance

### **Security Measures**
- **CSRF protection** on all forms
- **Authentication required** for sensitive operations
- **Input validation** and sanitization
- **SQL injection prevention** through Django ORM
- **XSS protection** through template escaping

### **Performance Optimizations**
- **Bulk database operations** for multiple reviews
- **Asynchronous word cloud generation**
- **Efficient database queries** with proper indexing
- **Static file serving** with WhiteNoise
- **Caching strategies** for recommendations

## 🚀 Deployment & Scalability

### **Current Deployment**
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **Environment**: Python 3.x compatible

### **Scalability Considerations**
- **Database**: Ready for PostgreSQL migration
- **Caching**: Redis integration ready
- **Load Balancing**: Stateless application design
- **CDN**: Static assets ready for CDN deployment
- **Microservices**: Modular architecture for service separation

## 📈 Analytics & Insights

### **User Analytics**
- **Review patterns** by category and sentiment
- **Recommendation effectiveness** tracking
- **User engagement** metrics
- **Category preference** analysis

### **System Analytics**
- **Sentiment distribution** across all reviews
- **Popular keywords** and phrases
- **Recommendation accuracy** metrics
- **Performance monitoring** data

## 🔮 Future Enhancements

### **Planned Features**
- **Advanced ML models** (BERT, RoBERTa) for better sentiment analysis
- **Collaborative filtering** for improved recommendations
- **Real-time notifications** for new recommendations
- **Social features** (review sharing, following)
- **Mobile app** development
- **Multi-language support**

### **Technical Improvements**
- **GraphQL API** for more flexible data fetching
- **WebSocket integration** for real-time updates
- **Advanced caching** with Redis
- **Microservices architecture** for better scalability
- **Docker containerization** for easy deployment

## 🏆 Hackathon Highlights

### **Innovation Points**
1. **Hybrid Sentiment Analysis**: Combines TextBlob with custom heuristics for better accuracy
2. **Intelligent Recommendation Engine**: Multi-factor scoring with diversity balancing
3. **Real-time Processing**: Instant sentiment analysis and recommendation updates
4. **Comprehensive Analytics**: Detailed insights into user preferences and review patterns
5. **Modern Tech Stack**: Latest Django version with modern frontend technologies

### **Technical Achievements**
- **100+ products** across 10 categories with realistic data
- **Sophisticated NLP pipeline** with emotion detection
- **Responsive, modern UI** with excellent UX
- **Scalable architecture** ready for production deployment
- **Comprehensive testing** and error handling

### **Business Value**
- **Customer Insights**: Deep understanding of user preferences
- **Personalization**: Tailored recommendations based on review history
- **Engagement**: Interactive dashboard encourages continued use
- **Scalability**: Ready for enterprise-level deployment
- **ROI**: Improved customer satisfaction through better recommendations

---

*This documentation provides a comprehensive overview of the Review Analyzer system, covering all technical aspects, features, and capabilities for hackathon judges and potential stakeholders.*
