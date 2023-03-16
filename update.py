import os
import time
from bs4 import BeautifulSoup as bs
from rich import print
import requests
from dataclasses import dataclass, asdict
import json


@dataclass
class Novels:
    title: str
    status: str
    chapters: str
    rating: str
    link: str
    image: str


url = "https://www.novelupdates.com"
nvlup = "https://www.novelupdates.com"
nvl_listing = "/novelslisting/?st=1&pg=1"

# 'sort by' categories
nvl_listing = "/novelslisting/?st=1&pg=1"
# sort
sort_by = ["1", "2", "3", "4", "5", "6", "7"]
order = ["1", "2"]
status = ["1", "2", "3", "4"]
search = "?s="
searchsep = '+'
search_end = "&post_type=seriesplans"

pathname = os.getcwd()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) "
    "Gecko/20100101 Firefox/103.0r"
}

failed_requests = []


def get_html(url):
    r = requests.get(url, headers=headers)
    # if our status code isn't out of range then get html
    if not r.ok:
        try:
            print(f'retrying {url}')
            time.sleep(2)
            r = requests.get(url, headers=headers)
            soup = bs(r.text, 'html.parser')
            return soup
        # if we get a failure then wait 20 seconds and try again
        except not r.ok:
            time.sleep(20)
            print(f'{url} failed')
            failed_requests.append(url)
    else:
        print(f'{r.status_code} success')
        soup = bs(r.text, 'html.parser')
        return soup


def get_search_html(count):
    url = f"https://www.novelupdates.com/novelslisting/?st=1&pg={count}"
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    return soup


def get_search(sort, order, status, count):
    url = f"{nvlup}/novelslisting/?sort={sort}&order={order}&status={status}"
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    return soup


def series_ranking(sort_ranking):
    ranks = ['series-ranking/', 'series-ranking/?rank=popular',
             'series-ranking/?rank=popmonth', 'series-ranking/?rank=sixmonths']
    rank_name = ['pop_weekly', 'pop_all', 'pop_month', 'pop_sixmonths']

    title = f"{rank_name[sort_ranking]}.json"
    sort = int(sort_ranking)
    url_rank = f"{url}/{ranks[sort]}"
    print(url_rank)
    print(title)
    # soup = get_html(url_rank)
    # parse_rank = parse_novel(soup)
    # to_json(parse_rank, title)


def parse_novel(html):
    novels = html.find_all('div', class_='search_main_box_nu')

    results = []
    for item in novels:
        new_item = Novels(
            title=item.find('a').text,
            status=item.find('div', class_="search_stats").text,
            chapters=item.find('span', class_='ss_desk').text,
            rating=item.find('div', class_='search_ratings').text,
            link=item.find('div', class_="search_title").find('a').get('href'),
            image=item.find('img', dp="yes").get('src')
        )
        results.append(asdict(new_item))
    return results


def to_json(res, title):
    print(res)

    with open(title, "w") as f:
        json.dump(res, f, indent=2)



def get_new_listings():
    for x in range(0, 2):
        html = get_search_html(x)
        res = parse_novel(html)
        to_json(res, "results.json")
        time.sleep(2)
        return res
    print(failed_requests)


get_new_listings()
