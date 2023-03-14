import argparse
from requests_html import HTMLSession

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser(
    prog="parse",
    description="simple html parsing tool for getting images, links and text.",
    epilog="Thanks for trying parse <3"
)

parser.add_argument("site")

parser.add_argument(
    "-l",
    "--links",
    action="store_true"
)

parser.add_argument(
    "-c",
    "--css",
    nargs="*"
)

parser.add_argument("-i", "--iter")

args = parser.parse_args()

# session = HTMLSession()

# request = session.get(args.site)
print(args)

links = args.links
css = args.css

session = HTMLSession()
request = session.get(args.site)
if links and not css:
    print(request.html.absolute_links)
else:
    element1 = args.css[0]
    print(element1)
    print(request.html.xpath(f'{element1}'))
