import argparse
import concurrent.futures
import threading
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = create_retry_session()
    return thread_local.session


BASE_DOMAIN = "https://classes.berkeley.edu"
BASE_URL = f"{BASE_DOMAIN}/search/class"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
MAX_WORKERS = 15
REQUEST_TIMEOUT = 25
SLEEP_INTERVAL = 0.1
RETRY_COUNT = 3
RETRY_BACKOFF = 0.5
STATUS_FORCELIST = (500, 502, 503, 504)


def create_retry_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=RETRY_COUNT,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=STATUS_FORCELIST,
        # method_whitelist=["HEAD", "GET", "OPTIONS"] # Use allowed_methods in newer urllib3
        allowed_methods=["HEAD", "GET", "OPTIONS"],  # Retry only for safe methods
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)  # Set default headers for the session
    return session


def scrape_page_urls(term_query_param: str, page_number: int):
    """
    Scrapes a single page of Berkeley class search results using a session with retries.
    """
    session = get_session()
    urls_on_page = []
    params = {"f[0]": f"term:{term_query_param}", "search": "", "page": page_number}

    try:
        time.sleep(SLEEP_INTERVAL)
        response = session.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        section_wrappers = soup.find_all("div", class_="st--section-name-wraper")
        section_wrappers = soup.select(
            "div.st--section-name-wrapper, div.st--section-name-wraper"
        )

        for wrapper in section_wrappers:
            link_tag = wrapper.find("a")
            if link_tag and "href" in link_tag.attrs:
                relative_url = link_tag["href"]
                if relative_url.startswith("/content/"):
                    full_url = BASE_DOMAIN + relative_url
                    urls_on_page.append(full_url)

    except requests.exceptions.RequestException as e:
        print(f" Final Request Error after retries for page {page_number}: {e}")
    except Exception as e:
        print(f" General Error processing page {page_number}: {e}")

    return page_number, urls_on_page


def scrape_all_pages_concurrent(args):
    """Scrapes all pages concurrently using ThreadPoolExecutor and retry sessions."""
    all_found_urls = set()
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for page_num in range(args.num_pages):
            futures.append(
                executor.submit(scrape_page_urls, args.term_query_param, page_num)
            )

        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=args.num_pages,
            desc="Scraping Pages",
        ):
            try:
                page_num_result, page_urls = future.result()
                if page_urls:
                    all_found_urls.update(page_urls)
                else:
                    print(f"No urls found for {page_num_result}")
            except Exception as exc:
                print(f" A task for a page generated an exception: {exc}")

    return list(all_found_urls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--term",
        help="Used for the output file name, ex. classes_fall2025.txt",
        type=str,
    )
    parser.add_argument(
        "--term_query_param",
        help="Used for the query params, go to classes.berkeley.edu and look at the url to find it, ex. 8573",
        type=str,
    )
    parser.add_argument(
        "--num_pages",
        help="Look at the number of pages on classes.berkeley.edu for a particular term",
        type=int,
    )
    args = parser.parse_args()

    print(f"Starting concurrent scraper for {args.num_pages} pages ({BASE_URL})...")
    print(
        f"Using {MAX_WORKERS} workers, {RETRY_COUNT} retries, backoff factor {RETRY_BACKOFF}s"
    )
    OUTPUT_FILENAME = f"berkeley_class_urls_{args.term}.txt"

    start_time = time.time()
    scraped_urls = scrape_all_pages_concurrent(args)
    end_time = time.time()

    print("-" * 30)
    print(f"Finished scraping URLs in {end_time - start_time:.2f} seconds.")
    print(f"Total unique URLs found: {len(scraped_urls)}")

    if scraped_urls:
        try:
            with open(OUTPUT_FILENAME, "w") as f:
                for url in sorted(scraped_urls):
                    f.write(url + "\n")
            print(f"\nURLs saved to {OUTPUT_FILENAME}")
        except OSError as e:
            print(f"\nError writing to file {OUTPUT_FILENAME}: {e}")
    else:
        print("\nNo URLs were successfully scraped.")
