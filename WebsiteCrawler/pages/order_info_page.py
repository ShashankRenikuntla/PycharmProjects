class OrderInfoPage:

    def __init__(self, page):

        self.page = page

        # Order Information heading
        self.order_information = page.locator(
            "label.active",
            has_text="2. Order Information"
        )

        # Grand Total
        self.grand_total = page.locator(
            "#finalPriceDynam"
        )

        # Checkout button
        self.checkout_button = page.locator(
            "#ButtonCheckout"
        )

    def is_loaded(self):

        return self.order_information.is_visible()

    def wait_until_loaded(self):

        self.order_information.wait_for(
            state="visible",
            timeout=15000
        )

    def get_order_information_text(self):

        return self.order_information.inner_text()

    def get_grand_total(self):

        return self.grand_total.inner_text()

    def click_checkout(self):

        self.checkout_button.click()