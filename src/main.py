from scraper import events, fighters, fights, fightstats, get_urls, normalise_tables


def main():

    print('Scrapes all urls from ufcstats.com')
    event_urls = get_urls.get_event_urls()
    get_urls.get_fight_urls(event_urls)
    get_urls.get_fighter_urls()

    print('Iterates through urls and scrapes key data into csv files')
    events.scrape_events()
    fights.scrape_fights()
    fightstats.scrape_fightstats()
    fighters.scrape_fighters()

    print('Normalises tables for clean final output')
    normalise_tables.normalise_tables()


if __name__ == '__main__':
    main()
