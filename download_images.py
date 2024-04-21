import pathlib
# from urllib.error import HTTPError
import os
# import urllib.request
import pandas as pd
import numpy as np
import requests # request img from web
import shutil
from tqdm import tqdm

def download_the_image(keyword,image_url, title):
    try:
        if image_url is not None:
            if os.path.exists(f"./images/{keyword}/{title}.jpg"):
                pass
            else:
                res = requests.get(image_url, stream = True)
                filename = f"./images/{keyword}/{title}.jpg"
                if res.status_code == 200:
                    with open(filename,'wb') as f:
                        shutil.copyfileobj(res.raw, f)
    except:
        pass

if __name__=='__main__':
    with open('/Users/vineethguptha/fhlbsf/topics.txt','r') as f:
        for line in f.readlines():
            topic = line.strip() #'Federal Home Loan Bank of San Francisco' #'First Republic Bank' #'fannie mae' # 'Federal Home Loan Bank of San Francisco'
            print(topic)
            pathlib.Path(f'/Users/vineethguptha/fhlbsf/images/{topic}').mkdir(parents=True, exist_ok=True)
            if os.path.exists(f'/Users/vineethguptha/fhlbsf/news/{topic}.csv'):
                df = pd.read_csv(f'/Users/vineethguptha/fhlbsf/news/{topic}.csv')
                for index, row in tqdm(df.iterrows()):
                    if row['image'] is not np.nan:
                        download_the_image(topic, row['image'], row['title'])
                        