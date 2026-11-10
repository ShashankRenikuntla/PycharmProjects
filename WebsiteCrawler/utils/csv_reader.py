import csv


class CSVReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_products(self):

        products = []

        with open(
            self.file_path,
            mode="r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                products.append(row)

        return products

    def get_expected_price(self, product_name):

        products = self.read_products()

        for product in products:

            if product["Product"] == product_name:
                return product["Expected_Price"]

        return None