# Web Scraper

A Python web scraper that extracts quotes from quotes.toscrape.com and saves them to a CSV file.

## Features
- Scrapes quotes, authors, and tags from multiple pages
- Handles pagination automatically
- Saves data to CSV format
- Includes error handling for network issues
- Respectful scraping with delays between requests

## Requirements
- Python 3.x
- requests library
- beautifulsoup4 library

## Installation
```bash
pip install requests beautifulsoup4
```

## How to Run
```bash
python main.py
```

## Output
The scraper will create a `quotes.csv` file containing:
- Quote text
- Author name
- Tags (comma-separated)

## Notes
- This scraper is for educational purposes only
- Always respect website terms of service and robots.txt
- Consider adding delays between requests to be polite to servers
