import requests, sys
from bs4 import BeautifulSoup
import litellm

from categories import categories
llm = ...

def get_page_content(url):
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_page_features(url):
    html_content = get_page_content(url)
    if not html_content:
        return None
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else "Unknown"
        meta_description = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and "content" in meta_tag.attrs:
            meta_description = meta_tag["content"]
        return {
            "url": url,
            "title": title,
            "meta_description": meta_description,
        }
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return None

def import_urls(txt):
    urls = []
    for line in txt.split("\n"):
        if "|" in line:
            urls.append(line.split("|")[0].strip())
    return urls

def categorize_item(item):
    prompt = f"Categorize this content into one of the following categories: {', '.join(categories)}\n\nTitle: {item['title']}\nDescription: {item['meta_description']}\nCategory:"
    response = llm.complete(prompt)
    
    category = response.strip()
    if category in categories:
        return category
    else:
        return "Uncategorized"

if __name__ == "__main__":
    print("enter your one-tab urls and press Ctrl-D:")
    urls = import_urls(sys.stdin.read())
    pages = []
    for url in urls:
        pages.append(extract_page_features(url))
