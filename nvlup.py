import os
import time
from bs4 import BeautifulSoup as bs
from rich import print
import requests
from dataclasses import dataclass, asdict
import json
import argparse
# import subprocess
# from dataclasses import dataclass
# from rich.console import Console, ConsoleOptions, RenderResult
# from rich.table import Table


parser = argparse.ArgumentParser()
parser.add_argument("--search", "-s",
                    help="search for a novel on Novelupdates",
                    nargs='?', default="False", action="store")
parser.add_argument("--rank", "-r", help="search for a novel on Novelupdates", nargs='?')
# parser.add_argument_group("ranking")
args = parser.parse_args()
print(args.search)

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
nvl_frequency = "/novelslisting/?sort=1&order=2&status=1"
nvl_rank = "/novelslisting/?sort=2&order=2&status=1"
nvl_rating = "/novelslisting/?sort=3&order=2&status=1"
nvl_readers = "/novelslisting/?sort=4&order=2&status=1"
nvl_reviews = "/novelslisting/?sort=6&order=2&status=1"
nvl_title = "/novelslisting/?sort=7&order=2&status=1"
nvl_lastupdate = "/novelslisting/?sort=8&order=2&status=1"
nvl_chapters = "/novelslisting/?sort=5&order=2&status=1"

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
    for x in range(0, 3):
        html = get_search_html(x)
        res = parse_novel(html)
        to_json(res, "results.json")
        time.sleep(2)
        return res
    print(failed_requests)


def gum_input(placeholder: str = None, password: bool = False):
    if not placeholder:
        if not password:
            result = os.popen(f"gum input")
        else:
            result = os.popen(f"./gum input --password")
        return result.read().replace(r"\n", "\n").strip()
    else:
        if not password:
            result = os.popen(f'gum input --placeholder "{placeholder}"')
        else:
            result = os.popen(f'gum input --password --placeholder "{placeholder}"')
        return result.read().replace(r"\n", "\n").strip()


def write(placeholder: str=None):
    if not placeholder:
        result = os.popen(f"gum write")
        return result.read().replace(r"\n", "\n").strip()
    else:
        result = os.popen(f'./gum write --placeholder "{placeholder}"')
        return result.read().replace(r"\n", "\n").strip()


if args.search is None:
    user_in = gum_input("search for a novel: ")
    if user_in is not None:
        print(user_in.replace(" ", "+"))
        series_ranking(0)
else:
    user_in = args.search.strip().replace(" ", "+")    
    print(user_in)

# get_new_listings()
