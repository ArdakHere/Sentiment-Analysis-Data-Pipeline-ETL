import html
import requests
from bs4 import BeautifulSoup
import re

def getAljazeeraNews(url):
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

    # Find all divs with class name containing "article"
    div_tags = soup.find_all('div', class_=re.compile(r'\barticle\b'))

    # Extract and clean text from span tags within those divs
    clean_texts = []
    for div in div_tags:
        span_tags = div.find_all('span')
        for span in span_tags:
            clean_texts.append(html.unescape(span.get_text()))

    return clean_texts


def getEuronews(url: str):
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
    # print(html_content)
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

print(getEuronews("https://www.euronews.com"))