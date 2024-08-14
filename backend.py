import json
import sys

from flask import Flask, request, jsonify, Response, stream_with_context
from nltk.corpus import stopwords

from data_ingestor import *
from flask_cors import CORS
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://ardakatagulov:gJ221JJ51LdfO3tr@cluster0.adqyl76.mongodb.net/")

app = Flask(__name__)
CORS(app)


@app.route('/ingest_data', methods=['GET'])
def ingest_data():
    guardian_list = getGuardianNews("https://www.theguardian.com")
    nytimes_list = getNYtimesnews("https://www.nytimes.com")
    bbc_list = getBBCnews("https://bbc.com")
    # nurkz_list = getNurkzNews("https://nur.kz")
    # tengrinews_list = getTengriNews("https://tengrinews.kz")
    # moscowtimes_list = getMoscowTimesNews("https://www.themoscowtimes.com")

    news_data_combined = {
        'guardian': guardian_list,
        'nytimes': nytimes_list,
        'bbc': bbc_list,
        # 'nurkz': nurkz_list,
        # 'tengrinews': tengrinews_list,
        # 'moscowtimes': moscowtimes_list
    }
    return jsonify(news_data_combined)


@app.route('/process_data', methods=['POST'])
def assign_sentiment_to_each_news():
    data = request.get_json()
    keys = data.keys()
    i = 0
    list = []
    for item in keys:
        news_texts = data.get(item, [])
        processed_data = assign_sentiment_data(item, news_texts)
        list.append(processed_data)
        i = i + 1

    return jsonify(list)


@app.route('/load_processed_data', methods=['POST'])
def load_processed_data():
    data = request.get_json()
    db = client["news_data"]
    collection = db["news_processed"]

    for item in data:
        for obj in item.values():
            print(obj)
            collection.insert_one(obj)

    return Response(status=200)


@app.route('/get_word_frequency', methods=['POST'])
def get_word_frequency():
    data = request.get_json()
    db = client["news_data"]
    collection = db["news_processed"]
    documents = collection.find()

    stop_words = set(stopwords.words('english'))  # Use nltk's stopwords list
    frequency_var = 0
    frequency_dict = {}
    freq = 0

    for entry in documents:
        title = entry['text']
        # Split the title into words, removing any non-alphanumeric characters
        words = re.findall(r'\b\w+\b', title.lower())

        for word in words:
            if word not in stop_words:  # Exclude stopwords
                if word not in frequency_dict:
                    frequency_dict[word] = {
                        'frequency': 1,
                        'associated_sentiment': entry['sentiment_index'],
                        'color': entry['color'],
                        'publisher': entry['publisher_identifier'],
                        'timestamp': entry['timestamp']
                    }
                else:
                    frequency_dict[word]['frequency'] += 1
                    avg_sentiment = (
                            (entry['sentiment_index'] + frequency_dict[word]['associated_sentiment'])
                            / frequency_dict[word]['frequency'])
                    frequency_dict[word]['associated_sentiment'] = avg_sentiment

    sorted_words = sorted(frequency_dict.items(), key=lambda item: item[1]['frequency'], reverse=True)

    # Get the top N frequent words, adjust N as needed
    top_n = 10  # For example, get the top 10 frequent words
    top_frequent_words = sorted_words[:top_n]

    print(top_frequent_words)
    return Response(status=200)


@app.route('/get_publisher_sentiment', methods=['GET'])
def get_publisher_sentiment():
    db = client["news_data"]
    collection = db["news_processed"]
    documents = collection.find()

    publisher_sentiments = {}
    for entry in documents:
        publisher = entry['publisher_identifier']
        sentiment = entry['sentiment_index']
        timestamp = entry['timestamp']

        if publisher not in publisher_sentiments:
            publisher_sentiments[publisher] = {
                'total_sentiment': sentiment,
                'count': 1,
                'latest_timestamp': timestamp  # Store the timestamp
            }
        else:
            publisher_sentiments[publisher]['total_sentiment'] += sentiment
            publisher_sentiments[publisher]['count'] += 1
            # Update the timestamp if the current one is more recent
            if timestamp > publisher_sentiments[publisher]['latest_timestamp']:
                publisher_sentiments[publisher]['latest_timestamp'] = timestamp

    # Calculate the average sentiment for each publisher and keep the timestamp
    for publisher in publisher_sentiments:
        avg_sentiment = publisher_sentiments[publisher]['total_sentiment'] / publisher_sentiments[publisher]['count']
        publisher_sentiments[publisher] = {
            'average_sentiment': avg_sentiment,
            'latest_timestamp': publisher_sentiments[publisher]['latest_timestamp']
        }

    print(publisher_sentiments)

    return jsonify(publisher_sentiments)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
