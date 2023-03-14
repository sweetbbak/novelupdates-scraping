import os
import sys
import subprocess
import requests
from rich import print
from bs4 import BeautifulSoup as bs
import json
from fzf import fzf_prompt
from fzf import Fzf

pathname = os.getcwd()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

urls = []


def choose(options: list, limit: bool = True):
    oxot = []
    for option in options:
        oxot.append(f'"{option}"')
    options = ' '.join(oxot)
    if not limit:
        result = os.popen(f"gum choose --no-limit {options}")
    else:
        result = os.popen(f"gum choose {options}")
    if not limit:
        return result.read().replace(r"\n", "\n").strip().split("\n")
    else:
        return result.read().replace(r"\n", "\n").strip()


def get_html(url):
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    soup = bs(r.text, 'html.parser')
    return soup


manga = []


def get_titles(html):
    reader = html.find_all('div', class_="relative flex space-x-2 rounded bg-white p-2 transition dark:bg-neutral-850")
    # reader = html.find('div', class_="grid grid-cols-1 gap-4 lg:grid-cols-4")

    for container in reader:
        image = container.find('div', class_="flex-shrink-0").find('a').find('img').get('src')
        link = container.find('div', class_="flex-shrink-0").find('a').get('href')
        title = container.find('div', class_="flex-shrink-0").find('a').find('img').get('alt')
        latest = container.find('div', class_="flex mt-2 space-x-2 mb-2").find('a').get('href')
        # to json maybe lol
        manga_info = {
            'title': title,
            'link': link,
            'latest': latest,
            'image': image
        }
        manga.append(manga_info)


def to_json():
    with open('/home/sweet/src/pyscrape/manga.json', 'w') as f:
        json.dump(manga, f)


def get_latest(url):
    html = get_html(url)
    get_titles(html)
    print(manga)


def parse_manga(url):
    images = []
    html = get_html(url)
    image_block = html.find_all('img', class_='max-w-full mx-auto display-block')
    for img in image_block:
        image_link = img.get('src')
        images.append(image_link)
        print(image_link)
    # return images
    # print(images)


def main():
    for x in urls:
        get_latest(x)
    to_json()


main()
