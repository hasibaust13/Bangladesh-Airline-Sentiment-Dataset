from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

links = []
next_link = []

browser = webdriver.Chrome('/home/towhid/twitter/chrome/chromedriver')
root_dir = "/home/towhid/twitter/outschool/tripadvisor"

links = ["https://www.tripadvisor.com/Airline_Review-d8729033-Reviews-Biman-Bangladesh-Airlines",
         "https://www.tripadvisor.com/Airline_Review-d10661140-Reviews-USBangla-Airlines",
         "https://www.tripadvisor.com/Airline_Review-d8729135-Reviews-Regent-Airways",
         "https://www.tripadvisor.com/Airline_Review-d15052989-Reviews-NOVOAIR"
         ]

next_link1 = [
    f"https://www.tripadvisor.com/Airline_Review-d8729033-Reviews-or{i}-Biman-Bangladesh-Airlines.html#REVIEWS"
    for i in range(5, 355, 5)]
next_link.extend(next_link1)
next_link2 = [
    f"https://www.tripadvisor.com/Airline_Review-d10661140-Reviews-or{i}-USBangla-Airlines.html#REVIEWS"
    for i in range(5, 120, 5)]
next_link.extend(next_link2)
next_link3 = [
    f"https://www.tripadvisor.com/Airline_Review-d8729135-Reviews-or{i}-Regent-Airways"
    for i in range(5, 130, 5)]
next_link.extend(next_link3)
next_link4 = [
    f"https://www.tripadvisor.com/Airline_Review-d15052989-Reviews-or{i}-NOVOAIR.html#REVIEWS"
    for i in range(5, 50, 5)]
next_link.extend(next_link4)


def find_info(soup):
    urls = []
    l_card = soup.find_all(
        'div', class_='glasR4aX')
    if len(l_card) > 1:
        try:
            for card in l_card:
                a = card.find_all('a')
                urls.append(a[0]['href'])
            return True, urls
        except Exception:
            return False, None
    else:
        return False, None


reviews = []
for li in tqdm(links):
    browser.get(li)
    time.sleep(2)

    # print(browser.page_source)
    filename = li.split('/')[-1]
    file_dir = os.path.join(root_dir, filename + '.html')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    c, r = find_info(soup)
    if c:
        reviews.extend(r)

df = pd.DataFrame()
df['review'] = reviews
df.to_csv('tripadvisor test.csv', index=False)

for li in tqdm(next_link):
    browser.get(li)
    time.sleep(2)

    # print(browser.page_source)
    filename = li.split('/')[-1]
    file_dir = os.path.join(root_dir, filename + '.html')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    c, r = find_info(soup)
    if c:
        reviews.extend(r)
    print(len(reviews))

df = pd.DataFrame()
df['review'] = reviews
df.to_csv('tripadvisor all.csv', index=False)
browser.close()
