import csv
from pathlib import Path


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
    file_path: Path, urls: list[str], fieldname: str
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
