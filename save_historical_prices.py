#!/usr/bin/env python3
import csv
import requests

from bs4 import BeautifulSoup
from http import HTTPStatus


URLS = [
    {
        'type': 'gold',
        'url': 'https://www.investing.com/commodities/gold-historical-data'
    },
    {
        'type': 'silver',
        'url': 'https://www.investing.com/commodities/silver-historical-data'
    }
]
FILE_NAME = 'prices.csv'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/'
                  '537.36'
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)

    if response.status_code != HTTPStatus.OK:
        raise Exception(response.status_code, response.content)

    return response.content


def parse_html(source_type, html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('#curr_table')[0].find_all('tr')
    prices = []

    for row in rows[1:]:  # skip table header
        timestamp_tag, price_tag, *_ = row.select('td')
        timestamp, price = timestamp_tag['data-real-value'], price_tag['data-real-value']
        prices.append({
            'timestamp': timestamp,
            'price': price,
            'type': source_type
        })

    return prices


def save_to_file(prices):
    headers = ['timestamp', 'price', 'type']

    with open(FILE_NAME, 'w') as f:
        csv_writer = csv.DictWriter(f, headers, lineterminator='\n')
        csv_writer.writeheader()
        csv_writer.writerows(prices)


def main():
    prices = []

    for source in URLS:
        html = get_html(source['url'])
        source_prices = parse_html(source['type'], html)
        prices += source_prices

    save_to_file(prices)

    print('Saved %s prices' % len(prices))


if __name__ == '__main__':
    main()
