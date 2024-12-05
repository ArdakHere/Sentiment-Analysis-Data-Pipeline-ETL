import logging

from data_utils.data_ingestor import getGuardianNews, getNYtimesnews, getBBCnews, getAljazeeraNews

def extract_webscraped_strings():

    try:
        guardian_list = getGuardianNews("https://www.theguardian.com")
    except Exception as e:
        logging.error(f"Failed to scrape Guardian: {e}")
        guardian_list = []

    try:
        nytimes_list = getNYtimesnews("https://www.nytimes.com")
    except Exception as e:
        logging.error(f"Failed to scrape NYtimes: {e}")
        nytimes_list = []

    try:
        bbc_list = getBBCnews("https://bbc.com")
    except Exception as e:
        logging.error(f"Failed to scrape BBC: {e}")
        bbc_list = []

    try:
        aljazeera_list = getAljazeeraNews("https://www.aljazeera.com")
    except Exception as e:
        logging.error(f"Failed to scrape Al-Jazeera: {e}")
        aljazeera_list = []

    news_data_combined = {
        'guardian': guardian_list,
        'nytimes': nytimes_list,
        'bbc': bbc_list,
        'aljazeera': aljazeera_list
    }

    return news_data_combined