# prompt: create a news aggregator site to host in Github Pages. scrape top 5 news sites for articles. After the articles have been scraped, display the links to headlines in Github pages site. when a user hovers over a news headline link, generate a summary and bullet list of key points for the article and display as a popup to the user. format the site page and the popup summary and key points to be aesthetically pleasing, clean, minimalist, practical and intuitive

# This script scrapes news articles and generates a basic HTML page for a news aggregator.
# Due to the complexity of the task, this script provides a simplified framework.  
# You will need to complete several parts and refine it significantly for a production-ready site.

import requests
from bs4 import BeautifulSoup
import re

# Replace with your actual news sources and CSS/JS.
news_sources = {
    "BBC": "https://www.bbc.com/news",
    "CNN": "https://www.cnn.com/",
    "NYT": "https://www.nytimes.com/",
    # ... add more sources
}

def scrape_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        # Example extraction (adjust according to the website's structure)
        headlines = soup.find_all("a", {"class": re.compile(r".*headline.*")}) # Adjust the regex

        articles = []
        for headline in headlines[:5]:  # Get the top 5 headlines
            title = headline.text.strip()
            link = headline.get("href")
            # Ensure absolute URLs
            if link and not link.startswith("http"):
                link = url + link
            articles.append({"title": title, "link": link})
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return []

def generate_html(news_data):
    # Basic HTML structure (expand this for styling and responsiveness)
    html = """<!DOCTYPE html>
<html>
<head>
<title>News Aggregator</title>
<style>
body { font-family: sans-serif; }
a { text-decoration: none; color: blue; }
.popup { display: none; position: absolute; border: 1px solid black; background-color: white; padding: 10px;}
</style>
</head>
<body>
<h1>News Headlines</h1>
<div id="news-container">"""

    for source, articles in news_data.items():
        html += f"<h2>{source}</h2>"
        for article in articles:
            html += f'<a href="{article["link"]}" onmouseover="showSummary(\'{article["link"]}\', this)" onmouseout="hideSummary(this)">{article["title"]}</a><br>\n'
            html += f'<div class="popup" id="popup-{article["link"].replace("/","-")}"></div>'
    
    html += """</div>
    <script>
    function showSummary(link, element) {
        const popup = document.getElementById('popup-' + link.replace("/", "-"));
        popup.style.display = 'block';
        popup.style.left = element.offsetLeft + 'px';
        popup.style.top = (element.offsetTop + element.offsetHeight) + 'px';
        // Here fetch the summary using JS and an API or NLP library
        popup.innerHTML = 'Fetching Summary...';
    }
    function hideSummary(element) {
        const popup = document.getElementById('popup-' + element.href.replace("/", "-"));
        popup.style.display = 'none';
    }
    </script>
</body>
</html>"""

    return html

# Main part
if __name__ == "__main__":
    all_news = {}
    for source, url in news_sources.items():
        articles = scrape_articles(url)
        all_news[source] = articles

    html_output = generate_html(all_news)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_output)

    print("index.html generated successfully.")
