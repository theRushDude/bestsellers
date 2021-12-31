import bs4
import json
import random
import pathlib
import mechanicalsoup as ms
import importlib.resources as resources
from datetime import date
import logging

from api import agents
browser = ms.Browser()
browser.set_user_agent(random.choice(agents))

pages = dict()
for file in pathlib.Path('.cache').glob('*'):
    with open(file, 'r') as f:
        cache_entry = json.loads(f.read())

    if (date.today() - date.fromisoformat(cache_entry['date'])).days >= 7:
        logging.log(5, f'Page older than 7 days. Url: {cache_entry["url"]}')

    pages[cache_entry['url']] = bs4.BeautifulSoup(cache_entry['html'], features='lxml')


def get(url: str) -> bs4.BeautifulSoup:
    # if the we do not have the page yet, we save it in the cache folder and add it to the dict
    if url not in pages:
        print(f'new request: {url}')
        response = browser.get(url)
        data = {'url': url, 'html': response.text, 'date': date.today().isoformat()}
        with open(f'.cache\\{random.randint(0, 16 ** 8):0>8X}.json', 'w') as f:
            f.write(json.dumps(data))

        pages[url] = response.soup

    if len(pages) % 10 == 0:
        browser.set_user_agent(random.choice(agents))

    return pages[url]
