import html

import requests
from bs4 import BeautifulSoup


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
    print(response.text)
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
    print(clean_texts)
    return clean_texts

print(getEuronews("https://www.euronews.com"))