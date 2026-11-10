# `crawler/url_crawler.py`
#
import time
from playwright.sync_api import Page
from urllib.parse import urljoin, urlparse


class URLCrawler:

    def __init__(self, page: Page, same_domain_only=True, timeout=30000):
        self.page = page
        self.same_domain_only = same_domain_only
        self.timeout = timeout

    def open_page(self, url):

        response = self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=self.timeout
        )

        print("Page opened:", self.page.url)
        print("Status:", response.status)

        # # Wait until the Desktop menu arrow is visible
        #
        # self.pages.get_by_role("link", name="Desktop").locator(
        #     ".menuarrows"
        # ).wait_for(
        #     state="visible",
        #     timeout=10000
        # )

       # print("Desktop menu arrow is visible - pages is ready")

    def check_url(self, url):

        try:
            start_time = time.perf_counter()

            response = self.page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=self.timeout
            )

            end_time = time.perf_counter()

            response_time = round(
                end_time - start_time,
                2
            )

            status = response.status

            if 200 <= status < 300:
                result = "PASS"

            elif 300 <= status < 400:
                result = "REDIRECT"

            elif 400 <= status < 500:
                result = "CLIENT_ERROR"

            elif 500 <= status < 600:
                result = "SERVER_ERROR"

            else:
                result = "UNKNOWN"

            print("URL:", url)
            print("Status:", status)
            print(
                "Response Time:",
                response_time,
                "seconds"
            )
            print("Result:", result)

            return {
                "url": url,
                "status": status,
                "result": result,
                "response_time": response_time
            }

        except Exception as e:

            print("URL:", url)
            print("Status: ERROR")
            print("Result: FAIL")
            print("Error:", e)

            return {
                "url": url,
                "status": "ERROR",
                "result": "FAIL",
                "response_time": None
            }

    def get_links(self):

        links = self.page.locator("a").all()

        valid_links = set()

        print("Total links Found:", len(links))

        base_domain = urlparse(
            self.page.url
        ).netloc

        for link in links:

            href = link.get_attribute("href")

            if not href:
                continue

            if href.startswith("#"):
                continue

            if href.startswith("mailto:"):
                continue

            if href.startswith("tel:"):
                continue

            if href.startswith("javascript:"):
                continue

            full_url = urljoin(
                self.page.url,
                href
            )

            if (
                self.same_domain_only
                and urlparse(full_url).netloc != base_domain
            ):
                continue

            valid_links.add(full_url)

        print(
            "Total <a> elements:",
            len(links)
        )

        print(
            "Valid URLs:",
            len(valid_links)
        )

        for url in valid_links:
            print(url)

        return valid_links
