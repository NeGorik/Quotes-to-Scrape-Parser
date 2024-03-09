# pip install requests parsel lxml
# pip install

import json
import requests
from parsel import Selector
from requests import Response



def parse(response: Response) -> list[dict]:
    selector = Selector(response.text)
    data = []

    quotes = selector.css(".quote")
    for quote in quotes:

        text = quote.css(".text::text").get().strip()[1:-1]
        author = quote.css("[itemprop='author']::text").get().strip()
        link = response.url + quote.css("span a::attr(href)").get()[1:]

        tags: list[dict] = [{
            "name": tag.css("::text").get().strip(),
            "link": response.url + tag.css("::attr(href)").get()[1:]
        }
            for tag in quote.css(".tags .tag")
        ]

        data.append({
            "text": text,
            "author": author,
            "tags": tags,
            "link": link
        })


    return data


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
}

url = 'https://quotes.toscrape.com'
response = requests.get(url=url, headers=headers)

quotes_to_scrape_data = parse(response)
print(json.dumps(quotes_to_scrape_data, indent=2, ensure_ascii=False))