# pip install requests parsel lxml

import json
import requests
from parsel import Selector, SelectorList
from requests import Response

def save_to_html(response, filename) -> None:
    with open(f'{filename}.html', 'w', encoding='utf-8') as file:
        file.write(response.text)


def read_from_html(filename) -> str:
    with open(f'{filename}.html', 'r') as file:
        html = file.read()

    return html


def parse(response: Response, headers: dict) -> list[dict]:
    data: list[dict] = []

    while True:
        selector: Selector = Selector(text=response.text)
        quotes: SelectorList = selector.css('.quote')
        for quote in quotes:
            text: str = quote.css('.text::text').get().strip()[1:-1]
            author: str = quote.css('[itemprop="author"]::text').get().strip()
            link: str = response.url + quote.css('span a::attr(href)').get()[1:]
            tags: list[dict] = [
                {
                    'name': tag.css('::text').get().strip(),
                    'link': response.url + tag.css('::attr(href)').get()[1:]
                }
                for tag in quote.css('.tags .tag')
            ]

            data.append({
                'text': text,
                'author': author,
                'link': link,
                'tags': tags
            })

        next_button: str = selector.css('.pager .next a::attr(href)').get()
        if next_button:
            url = 'https://quotes.toscrape.com' + next_button
            response: Response = requests.get(url=url, headers=headers)

        else:
            break

    return data


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
}

url = 'https://quotes.toscrape.com'

response: Response = requests.get(url=url, headers=headers)
save_to_html(response=response, filename='quotes')

quotes_to_scrape_data = parse(response, headers)
print(json.dumps(quotes_to_scrape_data, indent=2, ensure_ascii=False))
print(len(quotes_to_scrape_data))