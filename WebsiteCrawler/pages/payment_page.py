from datetime import datetime


class PaymentPage:

    def __init__(self, page):

        self.page = page

        # Card Number
        self.card_number = page.locator(
            "[name='CardNumber']"
        )

        # Expiry Month
        self.expiry_month = page.locator(
            "#ExpiryMonth"
        )

        # Expiry Year
        self.expiry_year = page.locator(
            "#ExpiryYear"
        )

        # CVV
        self.cvv = page.locator(
            "#CvvNumber"
        )

        # Name on Card
        self.name_on_card = page.locator(
            "#NameOnCard"
        )

        # Terms & Conditions
        self.terms_checkbox = page.locator(
            "#TermsAndConditionsChckbxId"
        )

        # Pay button
        self.pay_button = page.locator(
            "input[type='submit'][value^='Pay $']"
        )

        # Order Total
        self.order_total = page.locator(
            "span.prod_price"
        )

    def get_order_total(self):

        return self.order_total.inner_text()

    def is_loaded(self):

        return "/store/payment" in self.page.url

    def enter_card_number(self, card_number):

        self.card_number.fill(card_number)

    def select_current_expiry_date(self):

        current_date = datetime.now()

        current_month = current_date.month
        current_year = current_date.year

        month_value = f"{current_month:02d}"
        year_value = str(current_year)

        self.expiry_month.select_option(month_value)
        self.expiry_year.select_option(year_value)

    def get_selected_expiry_month(self):

        return self.expiry_month.input_value()

    def get_selected_expiry_year(self):

        return self.expiry_year.input_value()

    def enter_cvv(self, cvv):

        self.cvv.fill(cvv)

    def enter_name_on_card(self, name):

        self.name_on_card.fill(name)

    def accept_terms(self):

        self.terms_checkbox.check()

    def click_pay(self):

        self.pay_button.click()