from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import re


def title(soup):
    a_list = soup.find_all('h2', class_='text_header')
    if len(a_list) == 1:
        return a_list[0].text.strip()
    return None


def content_(soup):
    a_list = soup.find_all('div', class_='text_content')
    if len(a_list) == 1:
        return a_list[0].text.strip()
    return None


def author(soup):
    a_list = soup.find_all('span', itemprop="author")
    if len(a_list) == 1:
        return a_list[0].text.strip()
    return None


def td(soup):
    in_list = ['Seat Comfort', 'Cabin Staff Service', 'Food & Beverages',
               'Inflight Entertainment', 'Ground Service', 'Value For Money',
               'Wifi & Connectivity']
    key = soup.find_all('td', class_="review-rating-header")
    key = key[0].text.strip()
    if key in in_list:
        value = soup.find_all('td', class_="review-rating-stars")
        value = len(value[0].find_all('span', class_="star fill"))
    else:
        value = soup.find_all('td', class_="review-value")
        value = value[0].text.strip()
    return key, value


def date_(soup):
    a_list = soup.find_all('time', itemprop="datePublished")
    if len(a_list) == 1:
        return a_list[0].text.strip()
    return None


def table_(soup):
    a_list = soup.find_all('tr')
    if len(a_list) > 0:
        return a_list
    else:
        print(soup)
    return None


def country(soup):
    a_list = soup.find_all('h3', class_="text_sub_header userStatusWrapper")
    if len(a_list) == 1:
        str_ = a_list[0].text.strip()
        try:
            res = re.findall(r"\(([A-Za-z _]+)\)", str_)
            res = res[0]
            return res
        except Exception as ex:
            return None
    return None


df = pd.read_csv('raw review.csv')
data = []

for idx, row in df.iterrows():
    print('>>')
    print(idx, row['airline'])
    temp = {}
    # print(row['airline'], row['raw_review'])
    soup = BeautifulSoup(row['raw_review'], 'lxml')

    temp['title'] = title(soup)
    temp['author'] = author(soup)
    temp['author_country'] = country(soup)
    temp['datePublished'] = date_(soup)

    split_str = content_(soup).split(' | ')
    if len(split_str) == 2:
        ver, content_str = split_str[0], split_str[1]
    else:
        content_str = content_(soup)
        ver = None
    temp['content'] = content_str
    temp['verified'] = ver

    table = table_(soup)
    try:
        for i in table:
            key, vlaue = td(i)
            temp[key] = vlaue
    except Exception as ex:
        print(table, '\n', ex)
    data.append(temp)
    # if idx == 65:
    #     break
    print(temp)
    print('--'*20)

df = pd.DataFrame()
df = df.append(data, True)

df.to_csv('clean review.csv', index=False)
print(df)
