🌟 Smart Review Analyzer & Recommender

An AI-powered web app that analyzes customer reviews to extract sentiment, highlight key insights, and recommend relevant products. Built for rapid prototyping and hackathons.

🔑 Features

Sentiment Analysis → Detects if reviews are positive, negative, or neutral using NLP (TextBlob + custom keyword patterns).

Keyword Insights → Word cloud + charts to visualize most common words and trends.

Product Recommendations → Suggests products based on user review preferences with TF-IDF + Cosine Similarity.

Interactive Dashboard → Clean charts (Chart.js), color-coded sentiments, and explainable recommendations.

🛠️ Tech Stack

Backend: Django + SQLite

NLP: TextBlob + custom keyword heuristics

Recommendation Engine: Scikit-learn (TF-IDF + Cosine Similarity, content-based filtering)

Frontend: Bootstrap 5 + Chart.js

Local Setup
1) Create venv and install deps
```
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

2) Run migrations and seed products
```
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py seed_products
```

3) Start server
```
.\.venv\Scripts\python manage.py runserver
```

4) Test
```
.\.venv\Scripts\python manage.py test
```

Pages
- `/` Home (hero + features)
- `/analyze/` Review input page
- `/dashboard/` Charts, word cloud, top words, recommendations
- `/about/`, `/team/`

📄 Pages

/ → Home (hero + features)

/analyze/ → Review Input Page (write a review, see sentiment & keywords)

/dashboard/ → Dashboard (charts, word cloud, top words, recommendations)

/about/, /team/ → Project + team details

🎨 Design Notes

Colors:

Primary: #2563EB (blue)

Positive: #16A34A (green)

Negative: #DC2626 (red)

Neutral: #FACC15 (yellow)


🚀 Why This Project?

Understanding customer reviews is messy. Our solution makes it simple by combining NLP-powered sentiment analysis with a lightweight recommendation engine to give both insights and suggestions in one place. Perfect for businesses to boost engagement and sales while keeping the UX simple and explainable.


