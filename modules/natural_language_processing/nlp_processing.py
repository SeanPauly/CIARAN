# nlp_processing.py

from textblob import TextBlob

def analyze_text(text):
    # Perform sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment

    # Return sentiment analysis results
    return {
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity
    }
