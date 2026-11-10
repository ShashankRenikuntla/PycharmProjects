import os
from dotenv import load_dotenv

from pages.payroll_desktop_page import PayrollDesktopPage
from pages.pricing_page import PricingPage
from pages.payroll_product_page import PayrollProductPage
from utils.csv_reader import CSVReader
from pages.shopping_page import ShoppingPage
from pages.login_page import LoginPage
from pages.order_info_page import OrderInfoPage
from pages.payment_page import PaymentPage


load_dotenv()


def test_pricing(page):

    # --------------------------------------------------
    # 1. Open Payroll Desktop
    # --------------------------------------------------

    page.goto(
        "http://checkmarkerptest.com/payroll-software/desktop",
        wait_until="commit"
    )

    # --------------------------------------------------
    # 2. Go to Pricing
    # --------------------------------------------------

    payroll_page = PayrollDesktopPage(page)
    payroll_page.click_pricing()

    # --------------------------------------------------
    # 3. Choose Payroll Software Pro+
    # --------------------------------------------------

    pricing_page = PricingPage(page)
    pricing_page.choose_pro()

    # --------------------------------------------------
    # 4. Product Page - Get Product Price
    # --------------------------------------------------

    product_page = PayrollProductPage(page)

    actual_price = product_page.get_product_price()

    print("Actual Product Price:", actual_price)

    # --------------------------------------------------
    # 5. Compare Price with CSV
    # --------------------------------------------------

    csv_reader = CSVReader("data/product_prices.csv")

    expected_price = csv_reader.get_expected_price(
        "Payroll Software Pro+"
    )

    print("Expected Product Price:", expected_price)

    assert float(actual_price) == float(expected_price), \
        "Product price does not match expected price."

    # --------------------------------------------------
    # 6. Select Platform - Windows
    # --------------------------------------------------

    product_page.click_platfrom_choose()

    # --------------------------------------------------
    # 7. Select 32-bit / Version
    # --------------------------------------------------

    product_page.click_version_bit()

    # --------------------------------------------------
    # 8. Add Product to Cart
    # --------------------------------------------------

    product_page.click_add_to_cart()

    # --------------------------------------------------
    # 9. Shopping Page
    # --------------------------------------------------

    shopping_page = ShoppingPage(page)

    actual_platform = shopping_page.get_platform()

    print("Shopping Platform:", actual_platform)

    assert actual_platform == "Platform : Windows", \
        "Shopping platform is not Windows."

    # --------------------------------------------------
    # 10. Proceed to Checkout
    # --------------------------------------------------

    shopping_page.click_proceed_to_checkout()

    print("URL after Proceed:", page.url)
    print("Page title:", page.title())

    # --------------------------------------------------
    # 11. Validate Order Information / Login
    # --------------------------------------------------

    login_page = LoginPage(page)
    order_info_page = OrderInfoPage(page)

    # --------------------------------------------------
    # Case 1: Already logged in
    # --------------------------------------------------

    if order_info_page.is_loaded():

        print("Order Information page loaded directly.")

    # --------------------------------------------------
    # Case 2: Login required
    # --------------------------------------------------

    elif login_page.is_loaded():

        print("Login page loaded.")

        username = os.getenv("CHECKMARK_USERNAME")
        password = os.getenv("CHECKMARK_PASSWORD")

        assert username, \
            "CHECKMARK_USERNAME is not configured."

        assert password, \
            "CHECKMARK_PASSWORD is not configured."

        login_page.login(username, password)

        print("Login submitted.")

        order_info_page.wait_until_loaded()

        assert order_info_page.is_loaded(), \
            "Order Information page did not load after login."

        print("Order Information page loaded after login.")

    # --------------------------------------------------
    # Unexpected page
    # --------------------------------------------------

    else:

        assert False, \
            "Neither Order Information page nor Login page was loaded."

    # --------------------------------------------------
    # 12. Order Information
    # --------------------------------------------------

    print(
        "Order Information heading:",
        order_info_page.get_order_information_text()
    )

    grand_total = order_info_page.get_grand_total()

    print("Grand Total:", grand_total)


    # --------------------------------------------------
    # 13. Complete Payment
    # --------------------------------------------------

    order_info_page.click_checkout()

    payment_page = PaymentPage(page)

    assert payment_page.is_loaded(), \
        "Complete Payment page did not load."

    print("Complete Payment page loaded.")

    # --------------------------------------------------
    # 14. Validate Payment Page Order Total
    # --------------------------------------------------

    payment_order_total = payment_page.get_order_total()

    print(
        "Payment Page Order Total:",
        payment_order_total
    )

    actual_grand_total = float(
        grand_total.replace("$", "").replace(",", "").strip()
    )

    actual_payment_order_total = float(
        payment_order_total.replace("$", "").replace(",", "").strip()
    )

    print(
        "Order Information Grand Total:",
        actual_grand_total
    )

    print(
        "Payment Page Order Total:",
        actual_payment_order_total
    )

    assert actual_payment_order_total == actual_grand_total, \
        "Payment Page Order Total does not match Order Information Grand Total."

    print("Order Total validation: PASS")

    # --------------------------------------------------
    # 15. Enter Card Number
    # --------------------------------------------------

    payment_page.enter_card_number(
        "4111111111111111"
    )

    # --------------------------------------------------
    # 16. Select Dynamic Expiry Month and Year
    # --------------------------------------------------

    payment_page.select_current_expiry_date()

    print(
        "Selected Expiry Month:",
        payment_page.get_selected_expiry_month()
    )

    print(
        "Selected Expiry Year:",
        payment_page.get_selected_expiry_year()
    )

    # --------------------------------------------------
    # 17. Enter CVV
    # --------------------------------------------------

    payment_page.enter_cvv(
        "123"
    )

    # --------------------------------------------------
    # 18. Enter Name on Card
    # --------------------------------------------------

    payment_page.enter_name_on_card(
        "Test Employer"
    )

    # --------------------------------------------------
    # 19. Accept Terms and Conditions
    # --------------------------------------------------

    payment_page.accept_terms()

    print("Payment details entered.")
    print("Terms and Conditions accepted.")

    # --------------------------------------------------
    # 20. Click Pay
    # --------------------------------------------------

    payment_page.click_pay()

    print("Pay button clicked.")
