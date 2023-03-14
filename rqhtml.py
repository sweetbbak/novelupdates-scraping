from requests_html import HTMLSession
from rich import print
import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type = argparse.FileType('r'), default = '-')
parser.add_argument('-u', '--url')

session = HTMLSession()

url = sys.stdin()

# r = session.get('https://manganato.com')
r = session.get(url)

print(r.html.links)
print(r.html.absolute_links)
about = r.html.find('#latest', first=True)
print(about.text)