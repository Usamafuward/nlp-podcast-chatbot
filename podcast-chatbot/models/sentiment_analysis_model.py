import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

class SentimentAnalysis:
    def __init__(self):
        # Ensure the VADER lexicon is downloaded
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon")

        # Initialize the sentiment analyzer from NLTK
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text and return both the sentiment category
        (positive, negative, neutral, sarcastic, humorous, angry) and the raw sentiment scores.
        """
        # Preprocess the text for tone detection
        preprocessed_text = self.preprocess_text(text)

        # Get the polarity scores for the text
        scores = self.analyzer.polarity_scores(preprocessed_text)

        # Determine the sentiment category based on the compound score
        compound_score = scores["compound"]
        sentiment = self.determine_sentiment_category(compound_score, preprocessed_text)

        # Return both the sentiment category and the detailed scores
        return {"sentiment": sentiment, "scores": scores}

    def preprocess_text(self, text):
        """
        Preprocess the input text for tone detection.
        This can include normalization, removing unnecessary punctuation, etc.
        """
        # Example preprocessing (add more as necessary):
        text = text.lower()  # Normalize case
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
        return text

    def determine_sentiment_category(self, compound_score, text):
        """
        Determine the sentiment category based on the compound score and text analysis.
        """
        if compound_score >= 0.05:
            sentiment = "positive"
        elif compound_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Detect sarcasm, humor, and anger using simple heuristics or keywords
        if "just kidding" in text or "sarcastic" in text:
            sentiment = "sarcastic"
        elif "funny" in text or "laugh" in text:
            sentiment = "humorous"
        elif "angry" in text or "furious" in text:
            sentiment = "angry"

        return sentiment
