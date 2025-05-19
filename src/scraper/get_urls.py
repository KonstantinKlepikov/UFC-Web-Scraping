import csv
import time
from pathlib import Path

import bs4
import requests
from requests.exceptions import ConnectionError

from scraper.constants import (
    CONNECTION_LOST_TIMOUT,
    CONNECTION_LOST_TRYING,
    EVENT_URLS,
    FIGHT_URLS,
    FIGHTER_URLS,
    TO_MANY_REQUESTS_TIMOUT,
    TO_MANY_REQUESTS_TRYING,
    USER_AGENT_HEADERS,
)


def write_urls_to_csv(file_path: Path, urls: list[str]) -> None:
    """Helper function to write URLs to a CSV file"""
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for url in urls:
            writer.writerow([url])


def get_event_urls() -> list[str]:
    """Scrapes url of each UFC event from ufcstats.com"""

    trying = 0
    print('Scraping event links from ufcstats.com')
    while True:
        try:
            main_url = requests.get(
                'http://ufcstats.com/statistics/events/completed?page=all'
            )
            main_event_soup = bs4.BeautifulSoup(main_url.text, 'lxml')

            # Adds href to list if href contains a link with keyword 'event-details'
            all_event_urls = [
                item.get('href')
                for item in main_event_soup.find_all('a')
                if isinstance(item.get('href'), str)
                and 'event-details' in item.get('href')
            ]

            write_urls_to_csv(EVENT_URLS, all_event_urls)
            print(len(all_event_urls), 'event links successfully scraped')
            return all_event_urls
        except ConnectionError:
            if trying == CONNECTION_LOST_TRYING:
                raise
            print('Scraping event timout')
            time.sleep(CONNECTION_LOST_TIMOUT)
            trying += 1
            continue


def get_fight_urls(event_urls: list[str]) -> None:
    """Scrapes url of each UFC fight from ufcstats.com"""

    trying = 0
    print('Scrapes fight URLs from event pages')
    while True:
        try:
            all_fight_urls = []
            for url in event_urls:
                event_url = requests.get(url)
                event_soup = bs4.BeautifulSoup(event_url.text, 'lxml')
                for item in event_soup.find_all(
                    'a', class_='b-flag b-flag_style_green'
                ):
                    all_fight_urls.append(item.get('href'))

            write_urls_to_csv(FIGHT_URLS, all_fight_urls)
            print(len(all_fight_urls), 'fight links successfully scraped')
            break
        except ConnectionError:
            if trying == CONNECTION_LOST_TRYING:
                raise
            print('Scraping fight timout')
            time.sleep(CONNECTION_LOST_TIMOUT)
            trying += 1
            continue


def get_fighter_urls() -> None:
    """Scrapes url of each UFC fighter from ufcstats.com"""

    print('Scraping fighter links from ufcstats.com')

    # Creates a list of each fighter page alphabetically
    main_url_list: list[requests.Response] = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        trying = 0
        print(f'Try to parse {letter=}, {trying=}')
        while True:
            try:
                response = requests.get(
                    f'http://ufcstats.com/statistics/fighters?char={letter}&page=all',
                    headers={'User-agent': USER_AGENT_HEADERS},
                )
                if response.status_code == 429:
                    if trying == TO_MANY_REQUESTS_TRYING:
                        print(f'To much 429 for letter {letter}')
                        break
                    time.sleep(TO_MANY_REQUESTS_TIMOUT)
                    trying += 1
                    continue

                main_url_list.append(response)
                time.sleep(1)
                break
            except ConnectionError:
                if trying == CONNECTION_LOST_TRYING:
                    raise
                print('Scraping fighter urls timout')
                time.sleep(CONNECTION_LOST_TIMOUT)
                trying += 1
                continue

    main_soup_list = [bs4.BeautifulSoup(url.text, 'lxml') for url in main_url_list]
    fighter_urls = []
    for main_link in main_soup_list:
        for link in main_link.select('a.b-link')[1::3]:
            fighter_urls.append(link.get('href'))

    write_urls_to_csv(FIGHTER_URLS, fighter_urls)
    print(len(fighter_urls), 'links successfully scraped')
