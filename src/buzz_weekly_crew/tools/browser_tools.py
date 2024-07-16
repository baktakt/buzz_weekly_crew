from crewai_tools import tool
import feedparser 
import requests
from bs4 import BeautifulSoup
import json

class BrowserTools:

    def get_article_links(from_url: str, take: int) -> list:
        """
        Returns the selected number of article links
        found on the provided url
        """
        feed = feedparser.parse(from_url)        
        #articles = [{'title': entry.title, 'link': entry.link} for entry in feed.entries]
        # #return articles[:take]
        return feed.entries[:take]
    
    def read_website(website_url: str) -> str:
        """Read content from a webpage."""
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        return text_content[:2000]
    
    @tool
    def get_articles_from_feeds(rss_feeds_str: str, take: int = 3) -> str:
        """
        Returns the content of the selected number of articles from each RSS feed in the comma-separated string.
        """
        rss_feeds = [feed.strip() for feed in rss_feeds_str.strip().split(',')]
        all_articles = []
        for feed in rss_feeds:
            articles = BrowserTools.get_article_links(feed, take)
            for article in articles:
                # Extracting the required fields
                title = article.title,
                link = article.link,
                description = article.summary,
                pub_date = article.published,
                
                # Converting the article to a JSON string
                article_json = json.dumps({
                    'title': title,
                    'link': link,
                    'description': description,
                    'publish_date': pub_date,
                })
                
                # Adding the JSON string to the final list
                all_articles.append(article_json)
        
        return json.dumps(all_articles, indent=2)
        