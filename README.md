Smart Review Analyzer & Recommender

Tech
- Django (backend, SQLite)
- TextBlob + simple keyword emotions (NLP)
- Recommendation Engine: Scikit-learn (TF-IDF + Cosine Similarity for content-based filtering)
- Bootstrap 5 + Chart.js (frontend)

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

Notes
- Colors: primary #2563EB, positive #16A34A, negative #DC2626, neutral #FACC15
- Word cloud saved at `static/wordcloud.png` after analysis


