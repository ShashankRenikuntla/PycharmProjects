class PayrollDesktopPage:

    def __init__(self,page):
        self.page = page

        self.pricing_link = page.get_by_role(
            "link",
            name="Pricing",
            exact=True
        )

    def click_pricing(self):
        self.pricing_link.click()
