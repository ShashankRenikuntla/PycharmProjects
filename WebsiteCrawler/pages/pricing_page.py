class PricingPage:

    def __init__(self, page):
        self.page = page

        self.choose_pro_button = page.get_by_role(
            "link",
            name="Choose Pro+"
        )

    def choose_pro(self):
        self.choose_pro_button.click()