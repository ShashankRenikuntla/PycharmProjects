from crawler.url_crawler import URLCrawler
from reports.csv_report import CSVReport
from utils.url_comparator import URLComparator
from utils.text_compare import TextCompare
from utils.image_compare import ImageCompare
import json


def test_open_page(page):

    # ==========================================
    # LOAD CONFIGURATION
    # ==========================================

    page.set_viewport_size({
        "width": 1280,
        "height": 720
    })

    with open("config/crawler_config.json", "r") as file:
        config = json.load(file)

    staging_url = config["staging_url"]
    production_url = config["production_url"]
    same_domain_only = config["same_domain_only"]
    timeout = config["timeout"]
    output_file = config["output_file"]

    # ==========================================
    # STAGING
    # ==========================================

    staging_crawler = URLCrawler(
        page,
        same_domain_only=same_domain_only,
        timeout=timeout
    )

    staging_crawler.open_page(staging_url)

    # Wait for fonts
    staging_crawler.page.evaluate(
        "() => document.fonts.ready"
    )

    # Wait for images
    staging_crawler.page.wait_for_function(
        """() => Array.from(document.images)
        .every(img => img.complete)"""
    )

    # Wait for final rendering
    staging_crawler.page.wait_for_timeout(2000)

    # Full-pages screenshot
    staging_crawler.page.screenshot(
        path="reports/staging.png",
        full_page=True
    )

    # Get staging URLs
    staging_urls = staging_crawler.get_links()

    # ==========================================
    # PRODUCTION
    # ==========================================

    production_page = page.context.new_page()

    production_page.set_viewport_size({
        "width": 1280,
        "height": 720
    })

    production_crawler = URLCrawler(
        production_page,
        same_domain_only=same_domain_only,
        timeout=timeout
    )

    production_crawler.open_page(production_url)

    # Wait for fonts
    production_crawler.page.evaluate(
        "() => document.fonts.ready"
    )

    # Wait for images
    production_crawler.page.wait_for_function(
        """() => Array.from(document.images)
        .every(img => img.complete)"""
    )

    # Wait for final rendering
    production_crawler.page.wait_for_timeout(2000)

    # Full-pages screenshot
    production_crawler.page.screenshot(
        path="reports/production.png",
        full_page=True
    )

    # Get production URLs
    production_urls = production_crawler.get_links()

    # ==========================================
    # IMAGE COMPARISON
    # ==========================================

    image_comparator = ImageCompare(
        "reports/staging.png",
        "reports/production.png"
    )

    image_comparison = image_comparator.compare()

    # ==========================================
    # IMAGE COMPARISON REPORT
    # ==========================================

    print("================================")
    print("IMAGE COMPARISON REPORT")
    print("================================")

    print(
        "Changed Area:",
        f"{image_comparison['changed_percentage']:.2f}%"
    )

    print(
        "Threshold:",
        f"{image_comparison['threshold']:.2f}%"
    )

    print(
        "Result:",
        image_comparison["result"]
    )

    print("================================")

    # ==========================================
    # TEXT COMPARISON
    # ==========================================

    staging_text = staging_crawler.page.locator(
        "body"
    ).inner_text()

    production_text = production_crawler.page.locator(
        "body"
    ).inner_text()

    text_comparator = TextCompare(
        staging_text,
        production_text
    )

    text_comparison = text_comparator.compare()

    # ==========================================
    # TEXT COMPARISON REPORT
    # ==========================================

    print("================================")
    print("TEXT COMPARISON")
    print("================================")

    print(
        "Result:",
        text_comparison["result"]
    )

    print(
        "Staging Text Lines:",
        text_comparison["staging_lines"]
    )

    print(
        "Production Text Lines:",
        text_comparison["production_lines"]
    )

    print(
        "Differences in Staging:",
        len(text_comparison["missing_in_production"])
    )

    print(
        "Differences in Production:",
        len(text_comparison["extra_in_production"])
    )

    print("================================")

    # ==========================================
    # SHOW TEXT DIFFERENCES
    # ==========================================
    if text_comparison["result"] == "FAIL":

        print("TEXT DIFFERENCES")
        print("================================")

        difference_number = 1

        for difference in text_comparison["differences"]:
            print(
                f"Difference {difference_number}"
            )

            print(
                "STAGING    :",
                difference["staging"]
            )

            print(
                "PRODUCTION :",
                difference["production"]
            )

            print("--------------------------------")

            difference_number += 1

    else:

        print(
            "STAGING AND PRODUCTION TEXT MATCH"
        )

        print("================================")

    # ==========================================
    # OVERALL RESULT
    # ==========================================

    if (
            image_comparison["result"] == "PASS"
            and text_comparison["result"] == "PASS"
    ):
        overall_result = "PASS"
    else:
        overall_result = "FAIL"

    print("================================")
    print("WEB COMPARE PRO - LEVEL 1")
    print("================================")

    print(
        "Image Comparison:",
        image_comparison["result"]
    )

    print(
        "Text Comparison:",
        text_comparison["result"]
    )

    print(
        "Overall Result:",
        overall_result
    )

    print("================================")
    # ==========================================
    # URL COMPARISON
    # ==========================================

    comparator = URLComparator()

    comparison = comparator.compare(
        staging_urls,
        production_urls
    )

    print("================================")
    print("URL COMPARISON SUMMARY")
    print("================================")

    print(
        "Staging URLs:",
        len(staging_urls)
    )

    print(
        "Production URLs:",
        len(production_urls)
    )

    print(
        "Common URLs:",
        len(comparison["common"])
    )

    print(
        "Staging Only:",
        len(comparison["staging_only"])
    )

    print(
        "Production Only:",
        len(comparison["production_only"])
    )

    print("================================")

    # ==========================================
    # PRODUCTION URL CHECK
    # ==========================================

    results = []

    for url in production_urls:

        result = production_crawler.check_url(url)

        results.append(result)

    passed = sum(
        1
        for result in results
        if result["result"] == "PASS"
    )

    redirects = sum(
        1
        for result in results
        if result["result"] == "REDIRECT"
    )

    client_errors = sum(
        1
        for result in results
        if result["result"] == "CLIENT_ERROR"
    )

    server_errors = sum(
        1
        for result in results
        if result["result"] == "SERVER_ERROR"
    )

    failed = sum(
        1
        for result in results
        if result["result"] == "FAIL"
    )

    # ==========================================
    # WEBSITE CRAWL SUMMARY
    # ==========================================

    print("================================")
    print("WEBSITE CRAWL SUMMARY")
    print("================================")

    print(
        "Total URLs:",
        len(results)
    )

    print(
        "Passed:",
        passed
    )

    print(
        "Redirects:",
        redirects
    )

    print(
        "Client Errors:",
        client_errors
    )

    print(
        "Server Errors:",
        server_errors
    )

    print(
        "Failed:",
        failed
    )

    print("================================")

    # ==========================================
    # CSV REPORT
    # ==========================================

    report = CSVReport()

    report.write_report(
        results,
        output_file
    )