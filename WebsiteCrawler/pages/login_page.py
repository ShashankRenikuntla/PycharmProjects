class LoginPage:

    def __init__(self, page):
        self.page = page

        self.username = page.locator("#Email")
        self.password = page.locator("#Password")
        self.sign_in = page.locator("input[value='Sign In']")

    def is_loaded(self):

        return (
            "account/sign-in" in self.page.url
            and self.page.title() == "Sign In to Your CheckMark Account"
        )

    def login(self, username, password):

        self.username.fill(username)
        self.password.fill(password)

        self.sign_in.click()