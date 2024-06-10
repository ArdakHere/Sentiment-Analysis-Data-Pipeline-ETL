import requests
import json
from pip._internal.network import session

from data_processor import *
from data_ingestor import *

def perform_ingestion_and_processing_guardian(url: str):
    guardian_news = getGuardianNews(url)
    guardian_news_data = assign_sentiment_data('guardian', guardian_news)

    return guardian_news_data

def perform_ingestion_and_processing_nurkz(url: str):
    nurkz_news = getNurkzNews(url)
    nurkz_news_data = assign_sentiment_data('nurkz', nurkz_news)

    return nurkz_news_data

def perform_ingestion_and_processing_bbc(url: str):
    bbc_news = getBBCnews(url)
    bbc_news_data = assign_sentiment_data('bbc', bbc_news)

    return bbc_news_data

def perform_ingestion_and_processing_euronews(url: str):
    euronews_news = getEuronews(url)
    euronews_news_data = assign_sentiment_data('euronews', euronews_news)

    return euronews_news_data

def perform_ingestion_and_processing_tengrinews(url: str):
    tengrinews_news = getTengriNews(url)
    tengrinews_news_data = assign_sentiment_data('tengrinews', tengrinews_news)

    return tengrinews_news_data

def euronews_pipeline():
    url = 'http://localhost:8080/contentListener'
    data_ingested = perform_ingestion_and_processing_euronews("https://www.euronews.com/")
    data_processed = assign_sentiment_data('euronews', data_ingested)

    data_to_send = {}

    data_to_send['euronews_avg_sentiment'] = calculate_avg_sentiment_for_publisher(data_processed)

    response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(f"Successfully sent data: {data_to_send}")
    else:
        print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

    for title, attributes in data_processed.items():

        data_to_send = {
            'title': title,
            'publisher_identifier': attributes['publisher_identifier'],
            'sentiment_index': attributes['sentiment_index'],
            'color': attributes['color']
        }

        response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
        # if response.status_code == 200:
        #     print(f"Successfully sent data: {data_to_send}")
        # else:
        #     print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

def guardian_pipeline():
    url = 'http://localhost:8080/contentListener'
    data_ingested = perform_ingestion_and_processing_guardian("https://www.theguardian.com/international")
    data_processed = assign_sentiment_data('guardian', data_ingested)

    data_to_send = {}

    data_to_send['guardian_avg_sentiment'] = calculate_avg_sentiment_for_publisher(data_processed)

    response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(f"Successfully sent data: {data_to_send}")
    else:
        print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

    for title, attributes in data_processed.items():

        data_to_send = {
            'title': title,
            'publisher_identifier': attributes['publisher_identifier'],
            'sentiment_index': attributes['sentiment_index'],
            'color': attributes['color']
        }

        response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
        # if response.status_code == 200:
        #     print(f"Successfully sent data: {data_to_send}")
        # else:
        #     print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

def nurkz_pipeline():
    url = 'http://localhost:8080/contentListener'
    data_ingested = perform_ingestion_and_processing_nurkz("https://nur.kz")
    data_processed = assign_sentiment_data('nurkz', data_ingested)

    data_to_send = {}

    data_to_send['nurkz_avg_sentiment'] = calculate_avg_sentiment_for_publisher(data_processed)

    response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(f"Successfully sent data: {data_to_send}")
    else:
        print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

    for title, attributes in data_processed.items():

        data_to_send = {
            'title': title,
            'publisher_identifier': attributes['publisher_identifier'],
            'sentiment_index': attributes['sentiment_index'],
            'color': attributes['color']
        }

        response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})

        # if response.status_code == 200:
        #     print(f"Successfully sent data: {data_to_send}")
        # else:
        #     print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

def bbc_pipeline():
    url = 'http://localhost:8080/contentListener'
    data_ingested = perform_ingestion_and_processing_bbc("https://www.bbc.com")
    data_processed = assign_sentiment_data('bbc', data_ingested)

    data_to_send = {}

    data_to_send['bbc_avg_sentiment'] = calculate_avg_sentiment_for_publisher(data_processed)

    response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(f"Successfully sent data: {data_to_send}")
    else:
        print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

    for title, attributes in data_processed.items():

        data_to_send = {
            'title': title,
            'publisher_identifier': attributes['publisher_identifier'],
            'sentiment_index': attributes['sentiment_index'],
            'color': attributes['color']
        }

        response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
        # if response.status_code == 200:
        #     print(f"Successfully sent data: {data_to_send}")
        # else:
        #     print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

def tengrinews_pipeline():
    url = 'http://localhost:8080/contentListener'
    data_ingested = perform_ingestion_and_processing_tengrinews("https://tengrinews.kz")
    data_processed = assign_sentiment_data('tengrinews', data_ingested)

    data_to_send = {}

    data_to_send['tengrinews_avg_sentiment'] = calculate_avg_sentiment_for_publisher(data_processed)

    response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print(f"Successfully sent data: {data_to_send}")
    else:
        print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

    for title, attributes in data_processed.items():

        data_to_send = {
            'title': title,
            'publisher_identifier': attributes['publisher_identifier'],
            'sentiment_index': attributes['sentiment_index'],
            'color': attributes['color']
        }

        response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
        # if response.status_code == 200:
        #     print(f"Successfully sent data: {data_to_send}")
        # else:
        #     print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

# def moscowtimes_pipeline():
#     url = 'http://localhost:8080/contentListener'
#     data_ingested = perform_ingestion_and_processing_nurkz("https://www.themoscowtimes.com")
#     data_processed = assign_sentiment_data('moscowtimes', data_ingested)
#
#     data_to_send = {}
#
#     data_to_send['guardian_avg_sentiment'] = calculate_avg_sentiment_for_publisher(data_processed)
#
#     response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
#     if response.status_code == 200:
#         print(f"Successfully sent data: {data_to_send}")
#     else:
#         print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")
#
#     for title, attributes in data_processed.items():
#
#         data_to_send = {
#             'title': title,
#             'publisher_identifier': attributes['publisher_identifier'],
#             'sentiment_index': attributes['sentiment_index'],
#             'color': attributes['color']
#         }
#
#         response = requests.post(url, data=json.dumps(data_to_send), headers={'Content-Type': 'application/json'})
#         if response.status_code == 200:
#             print(f"Successfully sent data: {data_to_send}")
#         else:
#             print(f"Failed to send data: {data_to_send}. Status code: {response.status_code}, Response: {response.text}")

#print(calculate_avg_sentiment_for_publisher(data))

tengrinews_pipeline()
bbc_pipeline()
nurkz_pipeline()
guardian_pipeline()
euronews_pipeline()
