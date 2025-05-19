# UFC Web Scraping Script

Create root `poetry.toml` that looks like

```toml
virtualenvs.create = true
virtualenvs.in-project = true
```

Install dependencies and activate poetry environment

`poetry install --with dev --no-root`

Change `USER_AGENT_HEADERS` in `src/scraper/constants.py`

Install system `make` and use it for run scraper script

`make get`

Use `kaggle` cli to copy some notebooks for research data, if you wish.
