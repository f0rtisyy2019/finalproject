from bs4 import BeautifulSoup
import requests

def news_scrape(symbol):
    # initializing url
    base = 'https://www.barchart.com'
    quotes = '/quotes/'
    symbol_results = f'{base}{quotes}{symbol}'
    
    # setting up connection
    r = requests.get(symbol_results)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # error handling
    try:
        # where all recent news for symbol is located
        news_block = soup.find_all("div", class_="most-recent-stories")[0]

        # all news, grabbing first entry
        top_news_tag = news_block.find_all("div", class_="story")[0]

        # grabbing story link
        top_news = top_news_tag.find_all("a", class_="story-link")[0]

        # top news title
        title = top_news.text.strip()

        # top news link
        news_href = top_news['href']
        news_link = f'{base}{news_href}'

        news = dict()
        news['Title'] = title
        news['Link'] = news_link

        return news
    
    except:
        return(f"'{symbol}' is not valid, re-enter again.")

if __name__ == "__main__":
    print(news_scrape(symbol))