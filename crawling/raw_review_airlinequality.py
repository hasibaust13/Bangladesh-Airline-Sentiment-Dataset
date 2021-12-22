from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

browser = webdriver.Chrome('/your_directory/chromedriver')
liks_dict = {'Biman_Bangladesh_Airlines': 'https://www.airlinequality.com/airline-reviews/biman-bangladesh/?sortby=post_date%3ADesc&pagesize=100',
             'US_Bangla_Airlines': 'https://www.airlinequality.com/airline-reviews/us-bangla-airlines/?sortby=post_date%3ADesc&pagesize=100',
             'Regent_Airways': 'https://www.airlinequality.com/airline-reviews/regent-airways/?sortby=post_date%3ADesc&pagesize=100',
             'NOVOAIR': 'https://www.airlinequality.com/airline-reviews/novoair/?sortby=post_date%3ADesc&pagesize=20'}


def raw_review(soup):
    l_card = soup.find_all('article', itemprop="review")
    if len(l_card) > 1:
        return l_card
    else:
        return None


raws = []
airlines = []
for key, value in liks_dict.items():
    print(key)
    print(value)
    browser.get(value)
    time.sleep(1)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    raw = raw_review(soup)
    raws.extend(raw)
    airlines.extend([key for i in range(len(raw))])
    print(len(raw))

df = pd.DataFrame()
df['airline'] = airlines
df['raw_review'] = raws

df.to_csv('raw review.csv', index=False)
