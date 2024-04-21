import os
import re
import sys
import pathlib
import requests
import pandas as pd
import urllib.request
from tqdm import tqdm
from gnews import GNews
from urllib.error import HTTPError
from datetime import date, timedelta

def get_full_text(article, world_news_api):
    url = f"https://api.worldnewsapi.com/extract-news?analyze=true&url={article['url']}&api-key={world_news_api}"
    url_content = requests.get(url).json()
    return url_content

def get_all_articles_details(articles, keyword, count, old_titles):
    world_news_api_keys = ['e2a6486e9bd04518a72ceab6e01000bc', '94abfa23c141481183444a7379ef2fa0', '3b250e23bba34d2891eac90b69a86720','4af2293f37434a3d8a5b5475fac7b902','67a51008d5784036893b81e63d1010c5','75657f478d364257b863724177122af7','6cd87ff454854fdd8a166b98696b826e']
    index = 0
    with tqdm(total=len(articles)) as pbar:
        while index<len(articles):
            news = articles[index]
            if old_titles is not None:
                if news['title'] not in old_titles:
                    try:
                        article = get_full_text(news, world_news_api_keys[count])
                    except:
                        del articles[index]
                        continue
                else:
                    del articles[index]
                    continue
            else:
                try:
                    article = get_full_text(news, world_news_api_keys[count])
                except:
                    del articles[index]
                    continue
            try:
                count+=1
                if count==len(world_news_api_keys):
                    count=0
                news['content'] = article['text']
                news['image'] = article['image']
                news['publisher'] = news['publisher']['title']
                match = re.search(r'\d{4}-\d{2}-\d{2}', article['publish_date'])
                news['publish_date'] = match.group()
                news['default_sentiment'] = article['sentiment']
                news['entities'] = article['entities']
                index+=1
            except:
                del articles[index]
                pass
            pbar.update(1)
    return articles

def get_google_news(topic, count,old_titles,start_date):
    google_news = GNews(language='en', country='US', start_date=start_date, end_date=None)
    results = google_news.get_news(f'"{topic}"')
    print('Googling is done!',len(results))
    data = get_all_articles_details(results, topic, count,old_titles)
    return data

if __name__=='__main__':
    with open('/Users/vineethguptha/fhlbsf/topics.txt','r') as f:
        for line in f.readlines():
            topic = line.strip() #'Federal Home Loan Bank of San Francisco' #'First Republic Bank' #'fannie mae' # 'Federal Home Loan Bank of San Francisco'
            print(topic)
            start_date = date.today() - timedelta(days = 2)
            start_date = (start_date.year, start_date.month, start_date.day)
            filename = f'/Users/vineethguptha/fhlbsf/news/{topic}.csv'
            if os.path.exists(filename):
                old_df = pd.read_csv(filename)
                old_titles = old_df['title'].values
                df = pd.DataFrame(get_google_news(topic,0, old_titles, start_date = start_date))
                old_df = pd.read_csv(filename)
                df = pd.concat([old_df,df], ignore_index=True)
            else:
                old_df = pd.read_csv('/Users/vineethguptha/fhlbsf/news/First Republic Bank.csv')
                df = pd.DataFrame(get_google_news(topic,0, [], start_date = start_date),columns=old_df.columns)
            df.to_csv(filename,index=False)
