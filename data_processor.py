import ssl
import nltk
from deep_translator import GoogleTranslator

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

translator = GoogleTranslator(source='ru', target='en')

def assign_sentiment_color(polarity):

    if polarity > 0.3:
        return (0, 255, 0)  # Green for positive sentiment
    if 0.3 >= polarity > 0.15:
        return (196, 255, 0)
    if 0.15 >= polarity > 0:
        return (222, 255, 0)
    if polarity == 0:
        return (255, 239, 0)  # White for neutral sentiment
    if 0 > polarity > -0.15:
        return (255, 179, 0)
    if -0.15 >= polarity >= -0.3:
        return (255, 94, 0)
    if polarity < -0.3:
        return (255, 0, 0)  # Red for negative sentiment

def assign_sentiment_data(publisher: str, news_texts: dict) -> dict:

    processed_data = {}

    for article_text in news_texts:

        sentiment_index = analyzer.polarity_scores(article_text)
        color = assign_sentiment_color(sentiment_index['compound'])

        processed_data[article_text] = {
            'publisher_identifier': publisher,
            'sentiment_index': sentiment_index['compound'],
            'color': color
        }

    return processed_data

def calculate_avg_sentiment_for_publisher(data: dict) -> float:
    sentiment_values = [article['sentiment_index'] for article in data.values()]
    return sum(sentiment_values) / len(sentiment_values)