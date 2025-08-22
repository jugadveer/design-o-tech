from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from pathlib import Path
import re


EMOTION_KEYWORDS = {
	"happy": ["happy", "joy", "delight", "love", "great", "awesome"],
	"angry": ["angry", "hate", "rage", "furious", "worst", "terrible"],
	"sad": ["sad", "unhappy", "disappointed", "depress"],
	"surprised": ["surprised", "amazed", "shocked", "wow"],
}


def detect_emotion(text: str) -> str:
	text_lower = text.lower()
	for emotion, keywords in EMOTION_KEYWORDS.items():
		if any(k in text_lower for k in keywords):
			return emotion
	return "neutral"


def analyze_text(text: str) -> dict:
	# Base sentiment from TextBlob
	blob = TextBlob(text)
	polarity = float(blob.sentiment.polarity)
	subjectivity = float(blob.sentiment.subjectivity)

	# Heuristic overrides to better capture common negations and cues
	lower = text.lower()
	negative_patterns = [
		"didn't like", "didnt like", "don't like", "dont like", "do not like",
		"not good", "not great", "not worth", "not recommend", "do not recommend",
		"waste of", "poor quality", "broke", "broken", "terrible", "awful", "bad",
		"hate", "refund", "returning", "worst",
	]
	positive_patterns = [
		"love", "great", "excellent", "awesome", "amazing", "perfect", "fantastic",
	]

	neg_hit = any(pat in lower for pat in negative_patterns)
	pos_hit = any(pat in lower for pat in positive_patterns)

	if neg_hit and not pos_hit:
		sentiment = "negative"
		# Nudge polarity negative if blob missed it
		polarity = min(polarity, -0.2)
	elif pos_hit and not neg_hit:
		sentiment = "positive"
		polarity = max(polarity, 0.2)
	else:
		if polarity > 0.1:
			sentiment = "positive"
		elif polarity < -0.1:
			sentiment = "negative"
		else:
			sentiment = "neutral"
	emotion = detect_emotion(text)
	return {
		"polarity": polarity,
		"subjectivity": subjectivity,
		"sentiment": sentiment,
		"emotion": emotion,
	}


def generate_wordcloud(text: str, output_path: Path) -> None:
	if not text.strip():
		return
	# Tokenize and filter to avoid errors when only stopwords/short tokens are present
	words = re.findall(r"[a-zA-Z']+", text.lower())
	filtered = [w for w in words if len(w) >= 3 and w not in STOPWORDS]
	freq = {}
	for w in filtered:
		freq[w] = freq.get(w, 0) + 1
	if not freq:
		freq = {"reviews": 1}
	wc = WordCloud(width=800, height=400, background_color="white")
	wc.generate_from_frequencies(freq)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	wc.to_file(output_path)


