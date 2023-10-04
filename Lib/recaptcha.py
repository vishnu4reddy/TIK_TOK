from playwright.sync_api import Page
from PIL import Image
import pytesseract
import base64
import cv2
import numpy
import time


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open_login_page(self, url):
        self.page.goto(url)

    def enter_credentials(self, domain, username, password):
        self.page.locator("#domain").click()
        self.page.locator("#domain").fill(domain)
        self.page.locator("#userName").fill(username)
        self.page.locator("#password").fill(password)

    def fill_captcha_and_submit(self):
        captcha_image_selector = "#imgCaptcha"
        self.page.wait_for_selector(
            captcha_image_selector, state='visible', timeout=10000)

        captcha_image_data_url = self.page.evaluate(
            """(captchaImageSelector) => {
                const img = document.querySelector(captchaImageSelector);
                return img.src;
            }""",
            captcha_image_selector,
        )

        image_data = base64.b64decode(captcha_image_data_url.split(",")[1])
        grayscale_image = cv2.cvtColor(cv2.imdecode(
            numpy.frombuffer(image_data, numpy.uint8), -1), cv2.COLOR_BGR2GRAY)

        captcha_text = pytesseract.image_to_string(
            Image.fromarray(grayscale_image))

        self.page.locator("#captcha").fill(captcha_text)
        time.sleep(4)
        self.page.locator("button[type='submit']").click()
        return captcha_text.strip()
