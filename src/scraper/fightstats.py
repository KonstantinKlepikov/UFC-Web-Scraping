import csv
import time

import bs4
import requests

from scraper.constants import (
    FIGHT_FIELD,
    FIGHTSTATS_DATA_PATH,
    FIGHTSTATS_TABLE_ROWS,
    FIGHTSTATS_URLS,
    SHORT_TIMOUT,
)
from scraper.utils import (
    HttpException,
    HttpSolver,
    create_csv_file,
    filter_duplicate_urls,
    get_urls,
)


def get_fighter_id(fight_soup, fight_stats, fighter: int) -> str | None:
    """Scrapes fighter name"""
    if fighter == 1:
        try:
            return fight_stats[0].text
        except Exception:
            return fight_soup.select('a.b-fight-details__person-link')[0].text

    if fighter == 2:
        try:
            return fight_stats[1].text
        except Exception:
            return fight_soup.select('a.b-fight-details__person-link')[1].text

    return None


def get_striking_stats(
    fight_stats,
    fighter: int,
) -> tuple[str, str, str, str, str] | None:
    """Scrapes striking stats for specified fighter"""
    if fighter == 1:
        try:
            return (  # Knockdowns
                fight_stats[2].text,
                # Total strikes attempted
                fight_stats[8].text.split(' of ')[1],
                # Total strikes successful
                fight_stats[8].text.split(' of ')[0],
                # Significant strikes attempted
                fight_stats[4].text.split(' of ')[1],
                # Significant strikes successful
                fight_stats[4].text.split(' of ')[0],
            )

        except Exception:
            return (  # Knockdowns
                'NULL',
                # Total strikes attempted
                'NULL',
                # Total strikes successful
                'NULL',
                # Significant strikes attempted
                'NULL',
                # Significant strikes successful
                'NULL',
            )

    if fighter == 2:
        try:
            return (  # Knockdowns
                fight_stats[3].text,
                # Total strikes attempted
                fight_stats[9].text.split(' of ')[1],
                # Total strikes successful
                fight_stats[9].text.split(' of ')[0],
                # Significant strikes attempted
                fight_stats[5].text.split(' of ')[1],
                # Significant strikes successful
                fight_stats[5].text.split(' of ')[0],
            )

        except Exception:
            return (  # Knockdowns
                'NULL',
                # Total strikes attempted
                'NULL',
                # Total strikes successful
                'NULL',
                # Significant strikes attempted
                'NULL',
                # Significant strikes successful
                'NULL',
            )

    return None


def get_grappling_stats(
    fight_stats,
    fighter: int,
) -> tuple[str, str, str, str, str] | None:
    """Scrapes grappling stats for specified fighter"""
    if fighter == 1:

        try:
            return (  # Takedowns attempted
                fight_stats[10].text.split(' of ')[1],
                # Takedowns successful
                fight_stats[10].text.split(' of ')[0],
                # Submissions attempted
                fight_stats[14].text,
                # Reversals
                fight_stats[16].text,
                # Control time
                fight_stats[18].text,
            )

        except Exception:
            return (  # Takedowns attempted
                'NULL',
                # Takedowns successful
                'NULL',
                # Submissions attempted
                'NULL',
                # Reversals
                'NULL',
                # Control time
                'NULL',
            )

    if fighter == 2:

        try:
            return (  # Takedowns attempted
                fight_stats[11].text.split(' of ')[1],
                # Takedowns successful
                fight_stats[11].text.split(' of ')[0],
                # Submissions attempted
                fight_stats[15].text,
                # Reversals
                fight_stats[17].text,
                # Control time
                fight_stats[19].text,
            )

        except Exception:
            return (  # Takedowns attempted
                'NULL',
                # Takedowns successful
                'NULL',
                # Submissions attempted
                'NULL',
                # Reversals
                'NULL',
                # Control time
                'NULL',
            )

    return None


def scrape_fightstats() -> None:
    """Scrapes details of each UFC fight and appends to file 'ufc_fight_data.csv'"""

    urls = get_urls(FIGHTSTATS_URLS)
    urls = filter_duplicate_urls(FIGHTSTATS_DATA_PATH, urls, FIGHT_FIELD)

    if len(urls) == 0:
        print('Fightstats data already scraped.')
        return

    create_csv_file(FIGHTSTATS_DATA_PATH, FIGHTSTATS_TABLE_ROWS)

    print(f'Scraping {len(urls)} fightstats...')
    urls_scraped = 0

    with open(FIGHTSTATS_DATA_PATH, 'a+') as f:
        writer = csv.writer(f)

        for url in urls:

            solver = HttpSolver()
            print(f'Scrapes {url}')

            while True:
                try:
                    response = requests.get(url)
                    print(response.status_code)
                    if response.status_code == 429:
                        if solver.is_completely_429():
                            raise HttpException('429')

                    fight_soup = bs4.BeautifulSoup(response.text, 'lxml')
                    fight_stats = fight_soup.select('p.b-fight-details__table-text')

                    # Scrape fight stats for first fighter
                    fighter_name = get_fighter_id(fight_soup, fight_stats, 1)
                    (
                        knockdowns,
                        total_strikes_att,
                        total_strikes_succ,
                        sig_strikes_att,
                        sig_strikes_succ,
                    ) = get_striking_stats(fight_stats, 1)
                    (
                        takedown_att,
                        takedown_succ,
                        submission_att,
                        reversals,
                        ctrl_time,
                    ) = get_grappling_stats(fight_stats, 1)

                    # Add fight stats for first fighter to csv
                    writer.writerow(
                        [
                            fighter_name.strip(),
                            knockdowns.strip(),
                            total_strikes_att.strip(),
                            total_strikes_succ.strip(),
                            sig_strikes_att.strip(),
                            sig_strikes_succ.strip(),
                            takedown_att.strip(),
                            takedown_succ.strip(),
                            submission_att.strip(),
                            reversals.strip(),
                            ctrl_time.strip(),
                            url,
                        ]
                    )

                    # Scrape fight stats for second fighter
                    fighter_name = get_fighter_id(fight_soup, fight_stats, 2)
                    (
                        knockdowns,
                        total_strikes_att,
                        total_strikes_succ,
                        sig_strikes_att,
                        sig_strikes_succ,
                    ) = get_striking_stats(fight_stats, 2)
                    (
                        takedown_att,
                        takedown_succ,
                        submission_att,
                        reversals,
                        ctrl_time,
                    ) = get_grappling_stats(fight_stats, 2)

                    # Add fight stats for second fighter to csv
                    writer.writerow(
                        [
                            fighter_name.strip(),
                            knockdowns.strip(),
                            total_strikes_att.strip(),
                            total_strikes_succ.strip(),
                            sig_strikes_att.strip(),
                            sig_strikes_succ.strip(),
                            takedown_att.strip(),
                            takedown_succ.strip(),
                            submission_att.strip(),
                            reversals.strip(),
                            ctrl_time.strip(),
                            url,
                        ]
                    )

                    urls_scraped += 1
                    time.sleep(SHORT_TIMOUT)
                    break
                except IndexError as e:
                    print(f'Error scraping fightstate: {url}')
                    print(f'Error details: {e}')
                    break

                except ConnectionError:
                    if solver.is_completely_connection_lost():
                        raise HttpException('Connection lost')
                    continue

    print(f'{urls_scraped}/{len(urls)} links successfully scraped')
