import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

