#!/usr/bin/env python3
import csv
import statistics

from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime, timezone


FILE_NAME = 'prices.csv'
COMMODITY_TYPES = ['gold', 'silver']


def date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ArgumentTypeError('Date should have this format: YYYY-MM-DD')


def commodity(value):
    if value not in COMMODITY_TYPES:
        raise ArgumentTypeError('Commodity type should be one of: %s' % COMMODITY_TYPES)

    return value


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('start_date', type=date)
    parser.add_argument('end_date', type=date)
    parser.add_argument('commodity_type', type=commodity)

    arguments = parser.parse_args()
    return (
        arguments.start_date.replace(tzinfo=timezone.utc).timestamp(),
        arguments.end_date.replace(tzinfo=timezone.utc).timestamp(),
        arguments.commodity_type
    )


def read_prices(start_timestamp, end_timestamp, required_source_type):
    prices = []
    with open(FILE_NAME, 'r') as f:
        csv_reader = csv.reader(f)

        for index, row in enumerate(csv_reader):
            if index == 0:
                continue  # skip header

            timestamp, price, source_type = row
            if (
                source_type == required_source_type and
                start_timestamp <= float(timestamp) <= end_timestamp
            ):
                prices.append(price)

    return [float(price.replace(',', '')) for price in prices]


def main():
    start_timestamp, end_timestamp, source_type = parse_args()

    prices = read_prices(start_timestamp, end_timestamp, source_type)

    print('%s %s %s' % (source_type, statistics.mean(prices), statistics.variance(prices)))


if __name__ == '__main__':
    main()
