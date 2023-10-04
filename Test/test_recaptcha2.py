from Lib.recaptcha import LoginPage
from playwright.sync_api import Page


def test_login_recaptcha(page: Page):
    login_page = LoginPage(page)

    # Open the login page
    login_page.open_login_page(
        "https://app.keka.com/Account/UserNameLogin?returnUrl=%2F"
    )

    # Enter credentials
    login_page.enter_credentials("your_domain_name", "your_user_name", "your_password")

    # Fill CAPTCHA and submit
    login_page.fill_captcha_and_submit()
