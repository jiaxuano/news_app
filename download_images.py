import os
import shutil
import pathlib
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm


def download_the_image(keyword, image_url, title):
    """
    Download and save the image related to the article.

    Args:
        keyword (str): Keyword representing the topic.
        image_url (str): URL of the image to be downloaded.
        title (str): Title of the article.

    Returns:
        None
    """
    try:
        if image_url is not None:
            if os.path.exists(f"./images/{keyword}/{title}.jpg"):
                pass
            else:
                res = requests.get(image_url, stream=True)
                filename = f"./images/{keyword}/{title}.jpg"
                if res.status_code == 200:
                    with open(filename, 'wb') as f:
                        shutil.copyfileobj(res.raw, f)
    except Exception as e:
        pass


if __name__ == '__main__':
    with open('/Users/vineethguptha/fhlbsf/topics.txt', 'r') as f:
        for line in f.readlines():
            topic = line.strip()
            print(topic)
            pathlib.Path(f'/Users/vineethguptha/fhlbsf/images/{topic}')\
                .mkdir(parents=True, exist_ok=True)
            if os.path.exists(f'/Users/vineethguptha/fhlbsf/news/{topic}.csv'):
                df = pd.read_csv(f'/Users/vineethguptha/fhlbsf/news/\
                                 {topic}.csv')
                for index, row in tqdm(df.iterrows()):
                    if row['image'] is not np.nan:
                        download_the_image(topic, row['image'], row['title'])
