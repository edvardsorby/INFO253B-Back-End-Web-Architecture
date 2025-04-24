import argparse
import concurrent.futures
import threading
import time

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, ValidationError
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = create_retry_session()
    return thread_local.session


BASE_DOMAIN = "https://classes.berkeley.edu"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
MAX_WORKERS = 20
REQUEST_TIMEOUT = 30
SLEEP_INTERVAL = 0.05
RETRY_COUNT = 3
RETRY_BACKOFF = 0.5
STATUS_FORCELIST = (500, 502, 503, 504)


class ClassInfo(BaseModel):
    url: str
    term_name: str | None = None
    department: str | None = Field(None, alias="dept")
    course_number: str | None = None
    section_id: str | None = None
    course_title: str | None = None
    special_title: str | None = None
    instructor: str | None = None
    catalog_description: str | None = None
    class_description: str | None = None
    location: str | None = None


def create_retry_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=RETRY_COUNT,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=STATUS_FORCELIST,
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session


def scrape_class_details(url: str) -> ClassInfo | None:
    """Scrapes details for a single class page using a session with retries."""
    session = get_session()
    try:
        time.sleep(SLEEP_INTERVAL)
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        data = {"url": url}
        textbook_div = soup.find("div", attrs={"data-element": "textbook"})
        if textbook_div:
            data["term_name"] = textbook_div.get("data-term-name")
            data["dept"] = textbook_div.get("data-dept")
            data["course_number"] = textbook_div.get("data-course-number")
            data["section_id"] = textbook_div.get("data-section-id")

        course_title_tag = soup.find("h2", class_="sf--course-title")
        if course_title_tag:
            data["course_title"] = course_title_tag.get_text(strip=True)

        special_title_tag = soup.find("h3", class_="sf--special-title")
        if special_title_tag:
            data["special_title"] = special_title_tag.get_text(strip=True)

        instructor_p = soup.select_one("div.sf--instructors > p")
        if instructor_p:
            data["instructor"] = instructor_p.get_text(strip=True).strip()

        catalog_desc_section = soup.find("section", id="section-course-description")
        if catalog_desc_section:
            catalog_desc_div = catalog_desc_section.find(
                "div", class_="section-content"
            )
            if catalog_desc_div:
                data["catalog_description"] = catalog_desc_div.get_text(strip=True)

        class_desc_section = soup.find("section", id="section-class-description")
        if class_desc_section:
            class_desc_div = class_desc_section.find("div", class_="section-content")
            if class_desc_div:
                data["class_description"] = class_desc_div.get_text(strip=True)

        location_div = soup.find("div", class_="sf--location")
        if location_div:
            data["location"] = location_div.get_text(separator=" ", strip=True)

        try:
            return ClassInfo(**data)
        except ValidationError as e:
            print(f" Pydantic validation error for {url}: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f" Final Request Error after retries for detail page {url}: {e}")
        return None
    except Exception as e:
        print(f" General Error processing detail page {url}: {e}")
        return None


def process_urls_concurrent(urls: list[str], output_filename: str):
    """Processes a list of URLs concurrently and writes results to a JSONL file."""
    successful_scrapes = 0
    failed_urls = []

    with (
        concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor,
        open(output_filename, "w", encoding="utf-8") as outfile,
    ):
        future_to_url = {
            executor.submit(scrape_class_details, url): url for url in urls
        }

        for future in tqdm(
            concurrent.futures.as_completed(future_to_url),
            total=len(urls),
            desc="Scraping Class Details",
        ):
            url = future_to_url[future]
            try:
                class_data: ClassInfo | None = future.result()
                if class_data:
                    json_line = class_data.model_dump_json(exclude_none=True)
                    outfile.write(json_line + "\n")
                    successful_scrapes += 1
                else:
                    failed_urls.append(url)
            except Exception as exc:
                print(
                    f" URL {url} generated an exception during future processing: {exc}"
                )
                failed_urls.append(url)

    return successful_scrapes, failed_urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--term",
        help="Used for the output file name, ex. classes_fall2025.txt",
        type=str,
    )
    args = parser.parse_args()

    URL_INPUT_FILE = f"berkeley_class_urls_{args.term}.txt"
    OUTPUT_FILE = f"berkeley_class_details_{args.term}.jsonl"
    with open(URL_INPUT_FILE) as f:
        urls_to_scrape = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(urls_to_scrape)} URLs from {URL_INPUT_FILE}")

    if not urls_to_scrape:
        print("No URLs to process. Exiting.")
    else:
        print(f"\nStarting detailed scraping for {len(urls_to_scrape)} URLs...")
        print(
            f"Using {MAX_WORKERS} workers, {RETRY_COUNT} retries, backoff factor {RETRY_BACKOFF}s"
        )
        start_time = time.time()

        success_count, failures = process_urls_concurrent(urls_to_scrape, OUTPUT_FILE)

        end_time = time.time()
        print("-" * 30)
        print(f"Finished detailed scraping in {end_time - start_time:.2f} seconds.")
        print(
            f"Successfully scraped and wrote data for {success_count} classes to {OUTPUT_FILE}"
        )
        if failures:
            print(
                f"Failed to scrape or process {len(failures)} URLs (check logs or print failures list)."
            )
