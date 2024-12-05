import ssl
import nltk
from datetime import datetime

import pandas as pd
from nltk import FreqDist, word_tokenize
from nltk.corpus import stopwords
from pandas import DataFrame

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')
nltk.download('stopwords')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def assign_sentiment_color(polarity):

    if polarity > 0.3:
        return 0, 255, 0  # Green for positive sentiment
    if 0.3 >= polarity > 0.15:
        return 196, 255, 0
    if 0.15 >= polarity > 0:
        return 222, 255, 0
    if polarity == 0:
        return 255, 239, 0  # White for neutral sentiment
    if 0 > polarity > -0.15:
        return 255, 179, 0
    if -0.15 >= polarity >= -0.3:
        return 255, 94, 0
    if polarity < -0.3:
        return 255, 0, 0  # Red for negative sentiment


def assign_textual_sentiment(polarity):
    if polarity >= 0.5:
        return "positive"
    if 0.2 <= polarity < 0.5:
        return "mostly positive"
    if 0 < polarity < 0.2:
        return "slightly positive"
    if polarity == 0:
        return "neutral"
    if -0.2 < polarity < 0:
        return "slightly negative"
    if -0.5 < polarity <= -0.2:
        return "mostly negative"
    if polarity <= 0.5:
        return "negative"


def get_most_frequent_words(df):
    print("heyyyy")
    print(df.head())

    stop_words = set(stopwords.words('english'))

    merged_string = df['news_string'].str.cat(sep=' ')

    nltk.download('punkt')

    words = word_tokenize(merged_string.lower())

    # Filter out stop words
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    # Calculate frequency distribution of the filtered words
    fdist = FreqDist(filtered_words)

    filtered_fdist = fdist.most_common(20)
    print(filtered_fdist)
    return filtered_fdist




# def get_sentiment_to_word_frequency():
#     try:
#         db = client['news_data']
#         collection = db['news_processed']
#         documents = collection.find()
#
#         for item in documents:
#             print("Document fetched:", item)
#
#     except Exception as e:
#         print("Error occurred:", e)


def calculate_avg_sentiment_for_publisher(data: dict) -> float:
    sentiment_values = [article['sentiment_index'] for article in data.values()]
    return sum(sentiment_values) / len(sentiment_values)


