import os
import time
from bs4 import BeautifulSoup as bs
from rich import print
import requests
from dataclasses import dataclass, asdict
import json
from nvlup import choose, get_html, to_json 

@dataclass
class Novel:
    title: str
    description: str
    releases: list
    reviews: list

pathname = os.getcwd()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) "
    "Gecko/20100101 Firefox/103.0r"
}
 

def get_soup(url):
    soup = get_html(url)
    return soup


def open_soup(url):
    html = open("soup.html", "r")
    soup = html.read()
    soup = bs(soup, 'html.parser')
    # html.close()
    return soup


reviews = []
results = []


def get_title(soup):
    title = soup.find('div', "seriestitlenu").text
    return title
    

def get_chappies(soup):
    chapter_index = []
    linklist = []
    links = soup.find('div', class_="digg_pagination").find_all('a')
    if links is None:
        chapter_index.clear()
   
    for x in links:
        link = x.text
        linklist.append(link)
    # print(linklist)
    # i assume that the first entry is always 1 and the last is an arrow -> 
    # so we go -2 to get our pagination
    ranger = [1, int(linklist[-2])]
    # print(ranger)

    # get links on first page of chapters
    master = []
    table = soup.find_all('a', class_="chp-release")
    for y in table:
        link_td = y.get('href')
        master.append(link_td)
    # print("----------------")
    # print(master)
    # print("----------------")
    return master


def parse_reviews(soup):

    reviews = []
    # parse reviews
    review_base = soup.find('div', class_="w-comments-list")
    review_base = soup.find_all('div', class_="w-comments-item")
    for item in review_base:
        z = item.find
        z = item.select_one('div[class*="w-comments-item-text"]').text.strip()
        # print(z)
        reviews.append(z)
    return reviews


def description(soup):
    # parse description
    descriptions = []
    description_base = soup.find('div', class_="two-thirds")
    description_base = description_base.find_all('p')
    for scripts in description_base:
        xya = scripts.text
        descriptions.append(xya)
    description = ' '.join(map(str, descriptions))
       
    # print("----------------")
    # print(description)
    # print("----------------")
    return description


def get_all(soup):
    novel = []
    soup = soup
    desc = description(soup)
    # print(desc)
    reviews = parse_reviews(soup)
    # print(reviews)
    links = get_chappies(soup)
    # print(links)
    title = get_title(soup)
    # print(title)
    new_item = Novel(
        title=title,
        description=desc,
        releases=links,
        reviews=reviews,
    )
    novel.append(asdict(new_item))
    print(novel)
    with open("out.json", "w") as f:
        json.dump(novel, f)
    

def mainin(url):
    soup = get_soup(url)
    get_all(soup)
    

mainin("https://www.novelupdates.com/series/fake-saint-of-the-year/")
