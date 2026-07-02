from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus

from config import SEARCH_REGION, HEADLESS
from utils import clean_price


def search(search_term):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = (
            f"https://{SEARCH_REGION}.craigslist.org/"
            f"search/sss?query={quote_plus(search_term)}"
        )

        print(f"\nSearching: {url}\n")

        page.goto(url)
        page.wait_for_timeout(3000)

        rows = page.locator(".cl-search-result:not(.gallery-card)")
        row_count = rows.count()

        print(f"Found {row_count} listings")

        for i in range(row_count):
            row = rows.nth(i)

            try:
                title = row.locator(".posting-title .label").inner_text()
                price = row.locator(".priceinfo").inner_text()
                price = clean_price(price)
                location = row.locator(".result-location").inner_text()
                url = row.locator(".posting-title").get_attribute("href")

                results.append({
                    "title": title,
                    "price": price,
                    "location": location,
                    "url": url,
                    "source": "Craigslist",
                })

            except Exception:
                continue

        browser.close()

    return results