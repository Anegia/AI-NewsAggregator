# prompt: create a news aggregator site to host in Github Pages. the code must generate an index.html file to upload to Github Pages. scrape BBC and the Hill news sites for news articles involving Tech, US and World every 15 minutes. After the articles have been scraped, display the links to headlines in Github pages site. when a user hovers over a news headline link, generate a summary and bullet list of key points for the article and display as a popup to the user. format the site page and the popup summary and key points to be aesthetically pleasing, clean, minimalist, practical and intuitive. These are the URLs https://www.bbc.com/news and htttps://thehill.com/homenews/feed/

import requests
from bs4 import BeautifulSoup
import time
import datetime
import os

def scrape_bbc_news(keywords):
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if any(keyword in href.lower() or keyword in link.text.lower() for keyword in keywords):
          if "news" in href:
            articles.append({"title": link.text.strip(), "url": "https://www.bbc.com" + href if "http" not in href else href})
    return articles

def scrape_the_hill(keywords):
    url = "https://thehill.com/homenews/feed/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")  # Use xml parser for RSS feed
    
    articles = []
    for item in soup.find_all("item"):
        title = item.title.text
        link = item.link.text
        if any(keyword in title.lower() for keyword in keywords):
            articles.append({"title": title, "url": link})
    return articles


def generate_html(bbc_articles, the_hill_articles):
    html_content = """<!DOCTYPE html>
<html>
<head>
<title>News Aggregator</title>
<style>
body {
    font-family: sans-serif;
    margin: 20px;
    background-color: #f4f4f4;
}
.article-link {
    display: block;
    margin-bottom: 10px;
    padding: 10px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    cursor: pointer;
    position: relative;
}

.article-link:hover .tooltiptext {
    visibility: visible;
}
.tooltiptext{
  position: absolute;
  left: 105%; /* Position the tooltip text */
  top: 50%;
  transform: translateY(-50%);
  visibility: hidden;
  background-color: #555;
  color: #fff;
  text-align: left;
  padding: 5px 10px;
  border-radius: 6px;
  z-index: 1;
}
</style>
</head>
<body>
    <h1>News Headlines</h1>
    """


    for article in bbc_articles:
      html_content += f"<div class='article-link'><a href='{article['url']}'>{article['title']}</a><span class='tooltiptext'>Summary and key points will appear here</span></div>\n"  
    for article in the_hill_articles:
      html_content += f"<div class='article-link'><a href='{article['url']}'>{article['title']}</a><span class='tooltiptext'>Summary and key points will appear here</span></div>\n"

    html_content += "</body></html>"
    return html_content

if __name__ == "__main__":
    keywords = ["tech", "us", "world"]
    
    while True:
        bbc_news = scrape_bbc_news(keywords)
        the_hill_news = scrape_the_hill(keywords)
        
        html = generate_html(bbc_news, the_hill_news)
        with open("index.html", "w") as f:
          f.write(html)

        print(f"[{datetime.datetime.now()}] - Updated index.html")
        time.sleep(900) # 15 minutes