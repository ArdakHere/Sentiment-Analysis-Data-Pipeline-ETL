import re
from bs4 import BeautifulSoup
import requests
import ssl
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('vader_lexicon')
import html
from src.data_processor import *

analyzer = SentimentIntensityAnalyzer()


def getGuardianNews(url: str):

    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    translator = GoogleTranslator(source='ru', target='en')

    soup = BeautifulSoup(html_content, 'html.parser')

    unwanted_substrings = ["Toggle main menu",
                           "Toggle News",
                           "Toggle Opinion",
                           "Toggle Sport",
                           "Toggle Culture",
                           "Toggle Lifestyle",
                           "Search with Google",
                           "Toggle International edition"]


    # Extract text from aria-label attributes only if href is present and text does not contain unwanted substrings
    links = soup.find_all('a', attrs={'aria-label': True, 'href': True})
    clean_text = [
        html.unescape(link['aria-label'])
        for link in links
        if not any(substring in link['aria-label'] for substring in unwanted_substrings)
    ]
    return clean_text


def getNurkzNews(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    translator = GoogleTranslator(source='ru', target='en')

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with the specific classes
    article_links = soup.find_all('a', class_='js-article-link article-link')

    # Initialize the dictionary
    translated_texts = []

    # Populate the dictionary with extracted texts and placeholders
    for article_text in article_links:
        translated_text = translator.translate(article_text.get_text())
        translated_texts.append(translated_text)

    return translated_texts

def getBBCnews(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Define color assignment function

    # Extract and clean text from h2 tags
    h2_tags = soup.find_all('h2', attrs={'data-testid': 'card-headline'})
    clean_texts = [html.unescape(tag.get_text()) for tag in h2_tags]

    return clean_texts

def getEuronews(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    unwanted_substrings = ["Read more", "Log In", "wallpaper link", "My Account", "Euronews Logo"]

    # Extract text from aria-label attributes only if href is present and text does not contain unwanted substrings
    links = soup.find_all('a', attrs={'aria-label': True, 'href': True})
    clean_texts = [
        html.unescape(link['aria-label'])
        for link in links
        if not any(substring in link['aria-label'] for substring in unwanted_substrings)
    ]

    return clean_texts


def getTengriNews(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    spans = soup.find_all('span', class_='main-news_top_item_title')

    # Extract and clean text from nested a tags
    clean_texts = [html.unescape(span.find('a').get_text()) for span in spans if span.find('a')]

    translator = GoogleTranslator(source='ru', target='en')
    # Initialize the dictionary
    translated_texts = []

    for article_text in clean_texts:
        translated_text = translator.translate(article_text)
        translated_texts.append(translated_text)

    return translated_texts


def getMoscowTimesNews(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    spans = soup.find_all('span', class_='main-news_top_item_title')

    # Extract and clean text from nested a tags
    links_article_excerpt = soup.find_all('a', class_='article-excerpt-default__link')
    clean_texts = [html.unescape(link['title']) for link in links_article_excerpt]

    # Initialize the dictionary
    return clean_texts

def getNYtimesnews(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    spans = soup.find_all('span', class_='main-news_top_item_title')

    regex_pattern_summary = re.compile(r'summary-class css-\w+')
    regex_pattern_indicate = re.compile(r'indicate-hover css-\w+')

    clean_texts_summary = [html.unescape(p.get_text()) for p in soup.find_all('p', class_=regex_pattern_summary)]
    clean_texts_indicate = [html.unescape(p.get_text()) for p in soup.find_all('p', class_=regex_pattern_indicate)]

    # Initialize the dictionary
    data = {}

    clean_texts_total = clean_texts_indicate + clean_texts_summary

    return clean_texts_total

#print(getNurkzNews("https://nur.kz")) works

#print(getGuardianNews("https://www.theguardian.com/international")) works

#print(getBBCnews("https://bbc.com")) works

#print(getEuronews("https://www.euronews.com/")) works

#print(getTengriNews("https://tengrinews.kz"))

#print(getMoscowTimesNews("https://www.themoscowtimes.com/"))

#print(getNYtimesnews("https://www.nytimes.com/"))


# time, nytimes are accessible
# apnews are accessible -> for news titles use PagePromoContentIcons-Text