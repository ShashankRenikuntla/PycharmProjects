class ShoppingPage:

    def __init__(self, page):
        self.page = page

        self.platform = page.locator(
            "span",
            has_text="Platform : Windows"
        )

        self.product_amount = page.locator(
            "span.productTotal"
        )

        self.proceed_to_checkout = page.locator(
            "input[value='Proceed to Checkout']"
        )

    def get_platform(self):
        return self.platform.inner_text()

    def get_product_amount(self):
        return self.product_amount.inner_text()

    def click_proceed_to_checkout(self):
        self.proceed_to_checkout.click()