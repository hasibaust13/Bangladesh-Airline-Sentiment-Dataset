from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

links = []
next_link = []

browser = webdriver.Chrome('/your_directory/chromedriver')
root_dir = "/your_root_directory/tripadvisor"

root_link = "https://www.tripadvisor.com"
df = pd.read_csv('tripadvisor all.csv')
links = [root_link+i for i in df['review'].values]


def bubble(soup):
    l_card = soup.find_all(
        'span', class_="ui_bubble_rating", alt=True)
    print(l_card)
    if len(l_card) >= 1:
        return l_card[0]['alt']
    else:
        return None


def review_read(soup):
    l_card = soup.find_all('div',
                           class_='review hsx_review ui_columns is-multiline is-mobile inlineReviewUpdate provider0')
    if len(l_card) > 1:
        return True, l_card[0]
    else:
        return False, None


def title_read(soup):
    l_card = soup.find_all('span', class_='noQuotes')
    if len(l_card) == 1:
        return l_card[0].text
    else:
        return None


def re_read(soup):
    l_card = soup.find_all('p', class_='partial_entry')
    if len(l_card) == 1:
        return l_card[0].text
    else:
        return None


def travel_date(soup):
    l_card = soup.find_all('div', class_="prw_rup prw_reviews_stay_date_hsx")
    if len(l_card) == 1:
        return l_card[0].text
    else:
        return None


def ratingDate(soup):
    l_card = soup.find_all('span', class_="ratingDate relativeDate")
    if len(l_card) == 1:
        return l_card[0].text
    else:
        return None


rate = []
review_date = []
traveling_date = []
title = []
reviews = []
airlines = []

count = 0
for li in tqdm(links):
    print(li)
    browser.get(li)
    time.sleep(1)
    aline = li.split('-')[-2]

    soup = BeautifulSoup(browser.page_source, 'lxml')
    c, r = review_read(soup)
    if c:
        rate.append(bubble(soup))
        title.append(title_read(r))
        reviews.append(re_read(r))
        review_date.append(ratingDate(r))
        traveling_date.append(travel_date(r))
        airlines.append(aline)

df = pd.DataFrame()
df['title'] = title
df['review'] = reviews
df['review_date'] = review_date
df['travel_date'] = traveling_date
df['airline'] = airlines
df['rate'] = rate
print(df)
df.to_csv('tripadvisor review.csv', index=False)
browser.close()
