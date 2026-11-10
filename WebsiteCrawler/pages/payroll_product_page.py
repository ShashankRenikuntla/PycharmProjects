class PayrollProductPage:

    def __init__(self, page):
        self.page = page

        self.product_price = page.locator(
            "#PDSelectedSprtPlan2"
        )

        self.click_platfrom = page.locator("#PDWPlatform")

        self.click_version = page.locator("#PDW32PlatformVersion")

        self.add_to_cart_button = page.locator("#AddToCart")

    def get_product_price(self):
        return self.product_price.get_attribute("data-price")

    def click_platfrom_choose(self):
        self.click_platfrom.click()

    def click_version_bit(self):
        self.click_version.click()

    def click_add_to_cart(self):
        self.add_to_cart_button.click()
