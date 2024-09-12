import json
import sys
from collections import defaultdict, Counter
from datetime import timedelta

from fastapi import FastAPI, Depends, Request, HTTPException
from bson.json_util import dumps
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.database import engine, async_session_maker
from src.models.models import Base, NewsProcessed, NewsFrequencyWords
from src.data_ingestor import *

from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


app = FastAPI()

STOP_WORDS = {"the", "and", "is", "in", "of", "to", "a", "are", "how", "as", "from", "was", "were", "for", "t",
              "after", "this", "that", "these", "those", "there", "here", "where", "a", "b", "c", "d", "e", "f", "g",
              "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
              "when", "why", "what", "which", "who", "whom", "on", "at",
              "by", "with", "for", "about", "against", "between", "into",
              "through", "during", "before", "above", "below", "up", "down",
              "again", "further", "then", "once", "I", "you", "he", "she", "it",
              "we", "they", "me", "him", "her", "us", "them", "an", "or", "but", "s",
              "if", "so", "be", "been", "being", "have", "has", "had", "do", "does",
              "did", "will", "would", "shall", "should", "can", "could", "may", "might", "must"}


scheduler = BackgroundScheduler()


def run_driver_script():
    # Assuming driver.py is in the same directory or adjust the path accordingly
    subprocess.run(["python", "src/driver.py"])


# Schedule the task to run every day at 19:00 UTC
scheduler.add_job(run_driver_script, 'cron', hour=8, minute=50, second=0, timezone='UTC')
scheduler.start()


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@app.get('/')
def home():
    return "Hello World"


@app.get('/ingest_data')
async def ingest_data():
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
    return JSONResponse(content=news_data_combined, status_code=200)


@app.post('/process_data')
async def process_data(request: Request):
    data = await request.json()
    keys = data.keys()
    i = 0
    list = []
    for item in keys:
        news_texts = data.get(item, [])
        processed_data = assign_sentiment_data(item, news_texts)
        list.append(processed_data)
        i = i + 1

    return JSONResponse(content=list, status_code=200)


@app.post('/get_word_frequency')
async def get_word_frequency(request: Request):
    data = await request.json()
    word_frequencies = {}

    for text_object in data:
        for value in text_object.values():
            text = value.get('text', '')
            sentiment = value.get('sentiment_index', 0)
            timestamp = value.get('timestamp', '')

            # Tokenize the text and convert to lowercase
            words = re.findall(r'\b\w+\b', text)

            for word in words:
                if word == "US":
                    word = word.lower()
                    if word in word_frequencies:
                        word_frequencies[word]['frequency'] += 1
                        word_frequencies[word]['associated_sentiment'] = (
                                (word_frequencies[word]['associated_sentiment'] + sentiment)
                                / word_frequencies[word]['frequency']
                        )
                    else:
                        word_frequencies[word] = {
                            'associated_sentiment': sentiment,
                            'color': assign_sentiment_color(sentiment),
                            'frequency': 1,
                            'timestamp': timestamp,
                            'word': word,
                        }
                else:
                    word = word.lower()
                    print("Before stop check " + word)
                    if word.isalpha() and word not in STOP_WORDS:
                        print("After stop check " + word)
                        if word in word_frequencies:
                            word_frequencies[word]['frequency'] += 1
                            word_frequencies[word]['associated_sentiment'] = (
                                (word_frequencies[word]['associated_sentiment'] + sentiment)
                                / word_frequencies[word]['frequency']
                            )
                        else:
                            word_frequencies[word] = {
                                'associated_sentiment': sentiment,
                                'color': assign_sentiment_color(sentiment),
                                'frequency': 1,
                                'timestamp': timestamp,
                                'word': word,
                            }

    # Sort the words by frequency and get the top 20
    sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1]['frequency'], reverse=True)
    top_20_words = sorted_words[:20]

    # Convert top 20 words to list of dictionaries
    top_20_word_list = [
        {
            'word': word,
            'frequency': details['frequency'],
            'associated_sentiment': details['associated_sentiment'],
            'color': details['color'],
            'timestamp': details['timestamp'],
        }
        for word, details in top_20_words
    ]

    return JSONResponse(content=top_20_word_list, status_code=200)


@app.post('/load_processed_data/{collection_name}')
async def load_processed_data(collection_name: str, request: Request, session: AsyncSession = Depends(get_session)):

    if collection_name == "news_processed":
        # data = request.json()
        # db = client["news_data"]
        # collection = db[collection_name]  # Use the collection name passed in the URL
        # for item in data:
        #     for obj in item.values():
        #         collection.insert_one(obj)

        data = await request.json()
        for item in data:
            for obj in item.values():
                news_entry = NewsProcessed(
                    publisher_identifier=obj.get("publisher_identifier"),
                    sentiment_index=obj.get("sentiment_index"),
                    text=obj.get("text"),
                    timestamp=obj.get("timestamp"),
                    color=obj.get("color")
                )
                session.add(news_entry)

        await session.commit()

        return JSONResponse(content="Processed words loaded", status_code=200)

    if collection_name == "news_frequency_words":

        data = await request.json()
        for item in data:
                news_entry = NewsFrequencyWords(
                    associated_sentiment=item.get("associated_sentiment"),
                    color=item.get("color"),
                    frequency=item.get("frequency"),
                    timestamp=item.get("timestamp"),
                    text=item.get("word"),
                )
                session.add(news_entry)

        await session.commit()

        return JSONResponse(content="loaded", status_code=200)


@app.get('/get_processed_news_from_db')
def get_processed_news_from_db():
    db = client["news_data"]
    collection = db["news_processed"]
    documents = collection.find()

    documents_list = list(documents)
    json_data = dumps(documents_list)

    return JSONResponse(content=json_data, status_code=200)


@app.get('/get_frequency_data_from_db')
def get_frequency_words_from_db():
    db = client["news_data"]
    collection = db["news_frequency_words"]
    documents = collection.find()

    documents_list = list(documents)
    json_data = dumps(documents_list)

    return JSONResponse(content=json_data, status_code=200)


@app.get('/get_publisher_sentiments_from_db')
def get_avg_publisher_sentiment_from_db():
    db = client["news_data"]
    collection = db["news_avg_sentiment_by_publisher"]
    documents = collection.find({}, {'_id': 0})

    documents_list = list(documents)
    json_data = dumps(documents_list)

    return JSONResponse(content=json_data, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
