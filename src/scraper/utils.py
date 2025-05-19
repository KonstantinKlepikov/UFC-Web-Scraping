import csv
import time
from collections import Counter
from pathlib import Path

from scraper.constants import (
    CONNECTION_LOST_TIMOUT,
    CONNECTION_LOST_TRYING,
    TO_MANY_REQUESTS_TIMOUT,
    TO_MANY_REQUESTS_TRYING,
)


def create_csv_file(file_path: Path, table_rows: list[str]) -> None:
    """Creates csv file for scraped data"""
    if not file_path.exists():
        with open(
            file_path,
            'w',
            newline='',
            encoding='UTF8',
        ) as f:
            writer = csv.writer(f)
            writer.writerow(table_rows)
        print(f'Created {file_path.name}')
    else:
        print(f'Scraping to existing file {file_path.name}')


def filter_duplicate_urls(
    file_path: Path,
    urls: list[str],
    fieldname: str,
) -> list[str]:
    """Ensure each url is only scraped once when script is run multiple times"""
    if file_path.exists():
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            # List of previously scraped urls
            scraped_urls = [row[fieldname] for row in reader]
            # Removes scraped urls from event_urls
            for url in scraped_urls:
                if url in urls:
                    urls.remove(url)
    return urls


def get_urls(file_path: Path) -> list[str]:
    """Get urls for parsing"""
    if file_path.exists():
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            return [row[0] for row in reader]
    print(f'Missing file {file_path.name}')
    return []


class HttpException(Exception):
    """Проблемы с соединением"""


class HttpSolver(Counter):
    status_492 = 0
    connection_lost = 0

    def is_completely_connection_lost(self) -> bool:
        if self['connection_lost'] == CONNECTION_LOST_TRYING:
            return True
        print('Scraping connection lost timout')
        time.sleep(CONNECTION_LOST_TIMOUT)
        self['connection_lost'] += 1
        return False

    def is_completely_429(self) -> bool:
        if self['status_492'] == TO_MANY_REQUESTS_TRYING:
            return True
        print('Scraping 429 timout')
        time.sleep(TO_MANY_REQUESTS_TIMOUT)
        self['status_492'] += 1
        return False
