from bs4 import BeautifulSoup
from newspaper import Article
import requests
import articles
import re
import nltk
# nltk.download('all')

num_feeds = 10000
num_articles = 10000

def find_all_rss_feeds(URL, link_check=r"^http.*\.xml$"):
    page = BeautifulSoup(requests.get(URL).content, "html.parser")
    articleshtml = page.find_all("a")
    urls= []
    for i in articleshtml:
        if re.match(link_check, i.get("href", "")):
            urls.append(i.get("href"))
    return urls

def extract_articles_from_feed(feedurl, linktag="link"):
    pages = BeautifulSoup(requests.get(feedurl).content, "html.parser")
    items = [str(i.find(linktag).text) for i in pages.find_all("item")]
    
    def func(l, i):
        print("Getting article", i)
        article = Article(l)
        article.download()
        article.parse()
        return article
    
    return [func(l, i) for i,l in enumerate(items[:num_articles])]

def get_articles(URL, link_check=r"^http.*\.xml$", linktag="link"):
    rss_feeds = find_all_rss_feeds(URL, link_check)
    articles = []
    for feed in rss_feeds[:num_feeds]:
        articles.extend(extract_articles_from_feed(feed, linktag = linktag))
    return articles

"""
print("Ny times")
ny_articles = get_articles("https://www.nytimes.com/rss", linktag="guid")
all_articles = list(map(articles.Article, ny_articles))
print(sum(list(map(lambda i: i.save(), all_articles))))
print("BBC")
bbc_articles = get_articles("https://www.bbc.co.uk/news/10628494", linktag="guid")
all_articles = list(map(articles.Article, bbc_articles))
print(sum(list(map(lambda i: i.save(), all_articles))))
"""

print("Buzzfeed")
buzzfeed_articles = []
URL = "https://www.buzzfeed.com"
rss_feeds = find_all_rss_feeds(URL+"/rss", r".*\.xml")
for feed in rss_feeds[:5]:
    buzzfeed_articles.extend(extract_articles_from_feed(URL+feed, linktag="guid"))
all_articles = list(map(articles.Article, buzzfeed_articles))
print(sum(list(map(lambda i: i.save(), all_articles))))

"""
print("cipherbrief")
cipherbrief = extract_articles_from_feed("https://www.thecipherbrief.com/feed", linktag="guid")
all_articles = list(map(articles.Article, cipherbrief))
print(sum(list(map(lambda i: i.save(), all_articles))))

print("cnn")
cnn_articles = get_articles("https://edition.cnn.com/services/rss/", link_check=r".*\.rss", linktag="guid")
all_articles = list(map(articles.Article, cnn_articles))
print(sum(list(map(lambda i: i.save(), all_articles))))
"""

print("done")
