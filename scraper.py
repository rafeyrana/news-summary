from bs4 import BeautifulSoup as bs
import time
import requests
from transformers import T5Tokenizer, T5ForConditionalGeneration
def fetch(url):
    timeout_in_seconds = 3
    headers = {"user-agent": "Fake user-agent"}
    sleep_time_in_seconds = 1

    try:
        response = requests.get(
            url,
            timeout=timeout_in_seconds,
            headers=headers,
        )
        response.raise_for_status()
        time.sleep(sleep_time_in_seconds)

    except (requests.HTTPError, requests.ReadTimeout):
        return None

    else:
        return response.text
    
def scrape_updates(html_data):
    if not html_data:
        return []
    try:
        soup = bs(html_data, "html.parser")
        headers = soup.find_all("div", {"class": "more-story-inn"})
        urls = [header.find("a")["href"] for header in headers if header.find("a")]
    except Exception as e:
        print(f"Error in scrape_updates: {e}")
        return []
    return urls

def scrape_next_page_link(html_data):
    if not html_data:
        return None
    try:
        soup = bs(html_data, "html.parser")
        next_link = soup.find("a", {"class": "next page-numbers"})
        if next_link:
            return next_link["href"]
    except Exception as e:
        print(f"Error in scrape_next_page_link: {e}")
    return None

def scrape_news(html_data):
    if not html_data:
        return {}
    try:
        soup = bs(html_data, "html.parser")
        title = soup.find("h1").text
        meta = soup.find("ul",{"class": "article-meta"}).find_all('li')
        writer = meta[0].text
        time = meta[1].text
        content = soup.find("div",{"class": "story-content"}).get_text()
        content = ' '.join(content.strip().split())
        model_name = "t5-small"
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)
        inputs = tokenizer.encode("summarize: " + content, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=200, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return dict(
            title=title,
            writer=writer,
            timestamp=time,
            summary=summary
        )
    except Exception as e:
        print(f"Error in scrape_news: {e}")
        return {}

def get_tech_news(amount):
    url = "https://www.technewsworld.com/"
    news_list = []

    html_data = fetch(url)
    if not html_data:
        return []

    news_urls = scrape_updates(html_data)
    for url in news_urls[:amount]:
        print(url)
        news_page_html_content = fetch(url)
        if news_page_html_content:
            news_list.append(scrape_news(news_page_html_content))
    print(news_list)
    return news_list

news = get_tech_news(20)
print(news)