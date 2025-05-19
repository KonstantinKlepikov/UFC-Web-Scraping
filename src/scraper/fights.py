import csv
import re
import time

import bs4
import requests
from requests.exceptions import ConnectionError

from scraper.constants import (
    CONNECTION_LOST_TIMOUT,
    CONNECTION_LOST_TRYING,
    FIGHT_DATA_PATH,
    FIGHT_FIELD,
    FIGHT_TABLE_ROWS,
    FIGHT_URLS,
)
from scraper.utils import create_csv_file, filter_duplicate_urls, get_urls


def get_referee(overview) -> str:
    """Scrape referee name"""
    try:
        return overview[3].text.split(':')[1]
    except Exception:
        return 'NULL'


def get_fighters(fight_details, fight_soup):
    """Scrape both fighter names"""
    try:
        return fight_details[0].text, fight_details[1].text
    except Exception:
        return (
            fight_soup.select('a.b-fight-details__person-link')[0].text,
            fight_soup.select('a.b-fight-details__person-link')[1].text,
        )


def get_title_fight(fight_type) -> str:
    """Checks if fight is title fight"""
    return 'T' if 'Title' in fight_type[0].text else 'F'


def get_weight_class(fight_type) -> str:
    """Scrapes weight class of fight"""
    if 'Light Heavyweight' in fight_type[0].text.strip():
        return 'Light Heavyweight'

    if 'Women' in fight_type[0].text.strip():
        return "Women's " + re.findall(r'\w*weight', fight_type[0].text.strip())[0]

    if 'Catch Weight' in fight_type[0].text.strip():
        return 'Catch Weight'

    if 'Open Weight' in fight_type[0].text.strip():
        return 'Open Weight'

    try:
        return re.findall(r'\w*weight', fight_type[0].text.strip())[0]
    except Exception:
        return 'NULL'


def get_gender(fight_type) -> str:
    """Checks gender of fight"""
    return 'F' if 'Women' in fight_type[0].text else 'M'


def get_result(select_result, select_result_details):
    """Scrapes the way the fight ended (e.g. KO, decision, etc.)"""
    return (
        (
            select_result[0].text.split(':')[1].split()[0],
            select_result[0].text.split(':')[1].split()[-1],
        )
        if 'Decision' in select_result[0].text.split(':')[1]
        else (
            select_result[0].text.split(':')[1],
            select_result_details[1].text.split(':')[-1],
        )
    )


def scrape_fights() -> None:  # noqa: C901
    """Scrapes details of each UFC fight and appends to file 'ufc_fight_data.csv'"""

    urls = get_urls(FIGHT_URLS)
    urls = filter_duplicate_urls(FIGHT_DATA_PATH, urls, FIGHT_FIELD)

    if len(urls) == 0:
        print('Fight data already scraped.')
        return

    create_csv_file(FIGHT_DATA_PATH, FIGHT_TABLE_ROWS)

    print(f'Scraping {len(urls)} fights...')
    urls_scraped = 0

    with open(FIGHT_DATA_PATH, 'a+') as f:
        writer = csv.writer(f)

        for url in urls:

            trying = 0
            print(f'Scrapes {url}')
            while True:
                try:
                    fight_url = requests.get(url)
                    fight_soup = bs4.BeautifulSoup(fight_url.text, 'lxml')

                    # Define key select statements
                    overview = fight_soup.select('i.b-fight-details__text-item')
                    select_result = fight_soup.select(
                        'i.b-fight-details__text-item_first'
                    )
                    select_result_details = fight_soup.select('p.b-fight-details__text')
                    fight_details = fight_soup.select('p.b-fight-details__table-text')
                    fight_type = fight_soup.select('i.b-fight-details__fight-title')
                    win_lose = fight_soup.select('i.b-fight-details__person-status')

                    # Scrape fight details
                    event_name = fight_soup.h2.text
                    try:
                        referee = get_referee(overview)
                        f_1, f_2 = get_fighters(fight_details, fight_soup)
                    except AttributeError as e:
                        print(f'Skip this fight and move to the next one: {e}')
                        continue
                    num_rounds = overview[2].text.split(':')[1].strip()[0]
                    title_fight = get_title_fight(fight_type)
                    weight_class = get_weight_class(fight_type)
                    gender = get_gender(fight_type)
                    result, result_details = get_result(
                        select_result, select_result_details
                    )
                    finish_round = overview[0].text.split(':')[1]
                    finish_time = re.findall(r'\d:\d\d', overview[1].text)[0]
                    if (win_lose[0].text.strip() == 'W') | (
                        win_lose[1].text.strip() == 'W'
                    ):
                        if win_lose[0].text.strip() == 'W':
                            winner = f_1
                        else:
                            winner = f_2
                    else:
                        winner = 'NULL'

                    # Adds row containing scraped fight details to csv file
                    writer.writerow(
                        [
                            event_name.strip(),
                            referee.strip(),
                            f_1.strip(),
                            f_2.strip(),
                            winner.strip(),
                            num_rounds.strip(),
                            title_fight,
                            weight_class,
                            gender,
                            result.strip(),
                            result_details.strip(),
                            finish_round.strip(),
                            finish_time.strip(),
                            url,
                        ]
                    )

                    urls_scraped += 1
                    time.sleep(1)
                    break

                except ConnectionError:
                    if trying == CONNECTION_LOST_TRYING:
                        raise
                    print('Scraping fight timout')
                    time.sleep(CONNECTION_LOST_TIMOUT)
                    trying += 1
                    continue

    print(f'{urls_scraped}/{len(urls)} links scraped successfully')
