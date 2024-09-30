---
layout: post
title: "A simple Web Scraper in Python"
date: 2024-09-30
permalink: permalink: /posts/:title
categories: [Python Projects]
---

- The class  `WebScraper` implements a multithreaded web scraper that retrieves data from URLs, handles pagination, stores the data in an SQLite DB, and incorporates additional features such as custom exceptions, logging, decorators, shallow/deep copying, and data compression
- It has the  `Logging` module which is used throughout the scraper to provide information on the scraping process and to report errors. The  `log_method_call` decorator automatically logs whenever a method is called 
- It has the  `ScraeError` and  `URLFormatError` exceptions which handle scraping-related errors, such as failed HTTP requests or invalid URL formats, providing more control over error handling 
- The Scraper uses the  `threading` module to run multiple scraping operations concurrently. Each thread scrapes a different URL, speeding up the process. 


```python
import requests
from bs4 import BeautifulSoup
import threading
from itertools import islice
import gzip
import logging
from functools import wraps
import copy
import sqlite3
from urllib.parse import urljoin

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Custom Exception
class ScraperError(Exception):
    pass

class URLFormatError(ScraperError):
    """Custom exception for invalid URL format"""
    pass

# Decorator to log method calls
def log_method_call(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"Calling method: {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class WebScraper:
    def __init__(self, urls, db_name="scraped_data.db"):
        self._urls = urls  # List for URLs
        self._data = []  # List to hold scraped data
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    # Create a table to store scraped data in the database
    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS ScrapedData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    content TEXT
                )
            ''')
    
    # Save data to SQLite
    def save_to_db(self, url, content):
        with self.lock:  # Ensure only one thread can write to the DB at a time
            try:
                # Ensure content is not None and is a string
                if content is not None and content.strip() != "":
                    sanitized_content = str(content)  # Ensure it's a string
                    logging.info(f"Inserting URL: {url}, Content length: {len(sanitized_content)}")
                    self.conn.execute("INSERT INTO ScrapedData (url, content) VALUES (?, ?)", (url, sanitized_content))
                    self.conn.commit()
                    logging.info(f"Data saved to database for URL: {url}")
                else:
                    logging.warning(f"Skipped saving empty or None content for URL: {url}")
            except sqlite3.Error as e:
                logging.error(f"Error saving to database: {e}")

    # Getter and Setter for URLs using Python properties
    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, urls_list):
        if not all(isinstance(url, str) for url in urls_list):
            raise URLFormatError("All URLs must be strings.")
        self._urls = urls_list

    # Method for shallow copy (for illustration purposes)
    def get_shallow_copy(self):
        return copy.copy(self._data)

    # Method for deep copy
    def get_deep_copy(self):
        return copy.deepcopy(self._data)

    @log_method_call
    def fetch_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            raise ScraperError(f"Failed to fetch data from {url}")
        
        return response.text

    # Thread worker to handle each URL
    @log_method_call
    def scrape_url(self, url):
        try:
            html = self.fetch_data(url)
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            self._data.append((url, text))
            self.save_to_db(url, text)
            logging.info(f"Data scraped from {url}")
        except ScraperError as e:
            logging.error(f"ScraperError: {str(e)}")

    # Multithreading for scraping multiple URLs
    @log_method_call
    def run_scraper(self):
        threads = []
        for url in self._urls:
            thread = threading.Thread(target=self.scrape_url, args=(url,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

    # High-order function example: filtering content
    def filter_data(self, filter_func):
        return list(filter(filter_func, [data for _, data in self._data]))

    # Use sets for unique data processing
    def get_unique_data(self):
        return list(set([data for _, data in self._data]))

    # Dictionary to categorize data
    def categorize_data(self):
        categorized = {}
        for idx, (url, data) in enumerate(self._data):
            categorized[f"Page {idx+1} ({url})"] = data[:100]  # Store first 100 characters as summary
        return categorized

    # Data compression using gzip
    @log_method_call
    def compress_data(self):
        compressed_data = []
        for _, data in self._data:
            compressed = gzip.compress(data.encode())
            compressed_data.append(compressed)
        return compressed_data

    # Pattern matching (Python 3.10+)
    def match_url(self, url):
        match url:
            case str() if url.startswith("http://"):
                return "HTTP"
            case str() if url.startswith("https://"):
                return "HTTPS"
            case _:
                raise URLFormatError("Unsupported URL format")

    # Handling pagination (assuming /page/<number> URLs)
    def handle_pagination(self, base_url, num_pages=5):
        paginated_urls = [urljoin(base_url, f"page/{i}") for i in range(1, num_pages + 1)]
        return paginated_urls

# Usage of the scraper class
if __name__ == "__main__":
    base_url = "https://quotes.toscrape.com/"
    num_pages = 5  # Let's assume the website has 5 pages

    scraper = WebScraper([])

    # Handle paginated URLs
    paginated_urls = scraper.handle_pagination(base_url, num_pages)
    scraper.urls = paginated_urls

    # Scraping multiple paginated URLs with threading
    scraper.run_scraper()

    # Getting unique data using set
    unique_data = scraper.get_unique_data()
    logging.info(f"Unique Data: {unique_data}")

    # Shallow and Deep copying examples
    shallow_copy = scraper.get_shallow_copy()
    deep_copy = scraper.get_deep_copy()

    # Categorizing data
    categorized_data = scraper.categorize_data()
    logging.info(f"Categorized Data: {categorized_data}")

    # Compressing data
    compressed = scraper.compress_data()
    logging.info(f"Compressed data length: {len(compressed)}")

    # Example: Fetching data from the SQLite database
    with scraper.conn:
        rows = scraper.conn.execute("SELECT * FROM ScrapedData").fetchall()
        logging.info(f"Data in SQLite DB: {rows}")


```
