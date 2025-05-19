import csv
from datetime import datetime

import bs4
import requests

from scraper.constants import (
    FIGHTER_DATA_PATH,
    FIGHTER_FIELD,
    FIGHTER_TABLE_ROWS,
    FIGHTER_URLS,
)
from scraper.utils import create_csv_file, filter_duplicate_urls, get_urls


def parse_l_name(name: str) -> str:
    """Parse fighter last name depending on length of name"""
    if len(name) == 2:
        return name[-1]
    if len(name) == 1:
        return 'NULL'
    if len(name) == 3:
        return name[-2] + ' ' + name[-1]
    if len(name) == 4:
        return name[-3] + ' ' + name[-2] + ' ' + name[-1]
    return 'NULL'


def parse_nickname(nickname) -> str:
    if nickname.text == '\n':
        return 'NULL'
    return nickname.text.strip()


def parse_height(height) -> float | str:
    """Converts height in feet/inches to height in cm"""
    height_text = height.text.split(':')[1].strip()
    if '--' in height_text.split("'"):
        return 'NULL'
    height_ft = height_text[0]
    height_in = height_text.split("'")[1].strip().strip('"')
    return ((int(height_ft) * 12.0) * 2.54) + (int(height_in) * 2.54)


def parse_reach(reach) -> float | str:
    """Converts reach in inches to reach in cm"""
    reach_text = reach.text.split(':')[1]
    if '--' in reach_text:
        return 'NULL'
    return round(int(reach_text.strip().strip('"')) * 2.54, 2)


def parse_weight(weight_element) -> str:
    weight_text = weight_element.text.split(':')[1]
    if '--' in weight_text:
        return 'NULL'
    return weight_text.split()[0].strip()


def parse_stance(stance) -> str:
    stance_text = stance.text.split(':')[1]
    if stance_text == '':
        return 'NULL'
    return stance_text.strip()


def parse_dob(dob) -> str:
    """Converts string containing date of birth to datetime object"""
    dob_text = dob.text.split(':')[1].strip()
    if dob_text == '--':
        return 'NULL'
    return str(datetime.strptime(dob_text, '%b %d, %Y'))[0:10]


def scrape_fighters():
    """Scrapes details of each UFC fighter appends to CSV file 'ufc_fighter_data'"""

    urls = get_urls(FIGHTER_URLS)
    urls = filter_duplicate_urls(FIGHTER_DATA_PATH, urls, FIGHTER_FIELD)

    if len(urls) == 0:
        print('Fighter data already scraped.')
        return

    create_csv_file(FIGHTER_DATA_PATH, FIGHTER_TABLE_ROWS)
    urls_scraped = 0
    print(f'Scraping {len(urls)} fighters...')

    with open(FIGHTER_DATA_PATH, 'a+') as f:
        writer = csv.writer(f)

        # Iterates through each url and scrapes key details
        for url in urls:
            try:
                fighter_url = requests.get(url)
                fighter_soup = bs4.BeautifulSoup(fighter_url.text, 'lxml')

                name = fighter_soup.select('span')[0].text.split()
                nickname = fighter_soup.select('p.b-content__Nickname')[0]
                details = fighter_soup.select('li.b-list__box-list-item')
                record = (
                    fighter_soup.select('span.b-content__title-record')[0]
                    .text.split(':')[1]
                    .strip()
                    .split('-')
                )

                fighter_f_name = name[0]
                fighter_l_name = parse_l_name(name)
                fighter_nickname = parse_nickname(nickname)
                fighter_height_cm = parse_height(details[0])
                fighter_weight_lbs = parse_weight(details[1])
                fighter_reach_cm = parse_reach(details[2])
                fighter_stance = parse_stance(details[3])
                fighter_dob = parse_dob(details[4])
                fighter_w = record[0]
                fighter_l = record[1]
                fighter_d = record[-1][0] if len(record[-1]) > 1 else record[-1]
                fighter_nc_dq = (
                    record[-1].split('(')[-1][0] if len(record[-1]) > 1 else 'NULL'
                )

                # Adds new row to csv file
                writer.writerow(
                    [
                        fighter_f_name.strip(),
                        fighter_l_name.strip(),
                        fighter_nickname,
                        fighter_height_cm,
                        fighter_weight_lbs,
                        fighter_reach_cm,
                        fighter_stance,
                        fighter_dob[0:10],
                        fighter_w,
                        fighter_l,
                        fighter_d,
                        fighter_nc_dq,
                        url,
                    ]
                )

                urls_scraped += 1

            except IndexError as e:
                print(f'Error scraping fighter page: {url}')
                print(f'Error details: {e}')

    print(f'{urls_scraped}/{len(urls)} fighters scraped successfully')
