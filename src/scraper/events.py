import csv
import time
from datetime import datetime

import bs4
import requests

from scraper.constants import (
    CONNECTION_LOST_TIMOUT,
    CONNECTION_LOST_TRYING,
    EVENT_DATA_PATH,
    EVENT_FIELD,
    EVENT_TABLE_ROWS,
    EVENT_URLS,
)
from scraper.utils import create_csv_file, filter_duplicate_urls, get_urls


def scrape_events() -> None:
    """Scrapes details of each UFC event appends to CSV file 'ufc_event_data'"""

    urls = get_urls(EVENT_URLS)
    urls = filter_duplicate_urls(EVENT_DATA_PATH, urls, EVENT_FIELD)

    if len(urls) == 0:
        print('Event data already scraped or empty event urls file')
        return

    create_csv_file(EVENT_DATA_PATH, EVENT_TABLE_ROWS)

    print(f'Scraping {len(urls)} event URLs...')
    urls_scraped = 0

    with open(EVENT_DATA_PATH, 'a+') as f:
        writer = csv.writer(f)

        # Iterates through each event url to scrape key details
        for url in urls:

            trying = 0
            print(f'Scrapes {url}')

            while True:
                try:
                    event_request = requests.get(url)
                    event_soup = bs4.BeautifulSoup(event_request.text, 'lxml')
                    event_full_location = (
                        event_soup.select('li')[4].text.split(':')[1].strip().split(',')
                    )

                    event_name = event_soup.select('h2')[0].text
                    event_date = str(
                        datetime.strptime(
                            event_soup.select('li')[3].text.split(':')[-1].strip(),
                            '%B %d, %Y',
                        )
                    )
                    event_city = event_full_location[0]
                    event_country = event_full_location[-1]

                    # Check event location contains state details
                    if len(event_full_location) > 2:
                        event_state = event_full_location[1]
                    else:
                        event_state = 'NULL'
                    urls_scraped += 1

                    # Adds new row to csv file
                    writer.writerow(
                        [
                            event_name.strip(),
                            event_date[0:10],
                            event_city.strip(),
                            event_state.strip(),
                            event_country.strip(),
                            url,
                        ]
                    )
                except IndexError as e:
                    print(f'Error scraping events page: {url}')
                    print(f'Error details: {e}')
                    break

                except ConnectionError:
                    if trying == CONNECTION_LOST_TRYING:
                        raise
                    print('Scraping events timout')
                    time.sleep(CONNECTION_LOST_TIMOUT)
                    trying += 1
                    continue

    print(f'{urls_scraped}/{len(urls)} events successfully scraped')
