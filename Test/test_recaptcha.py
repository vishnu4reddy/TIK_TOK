from playwright.sync_api import Page
from PIL import Image
from Data.data_recaptcha import Domine_name, user_name, password
import pytesseract
import base64
import cv2
import numpy
import time

Domine_Name = Domine_name
User_name = user_name
Password = password


def test_extract_captcha_text(page: Page):
    # Replace with the actual URL of the page containing the CAPTCHA
    page.goto("https://app.keka.com/Account/UserNameLogin?returnUrl=%2F")

    # Define a mechanism to obtain the CAPTCHA text before filling it in.
    # captcha_text = get_captcha_text  # Replace with the correct implementation

    page.locator("#domain").click()
    page.locator("#domain").fill(Domine_Name)
    page.locator("#userName").fill(User_name)
    page.locator("#password").fill(Password)
    # page.locator("#captcha").fill(captcha_text)
    # page.locator("button[type='submit']").click()

    # Replace with the actual selector for the CAPTCHA image element
    captcha_image_selector = "#imgCaptcha"

    # Wait for the CAPTCHA image to load (adjust timeout as needed)
    page.wait_for_selector(captcha_image_selector,
                           state="visible", timeout=10000)

    # Use JavaScript to extract the data URL of the CAPTCHA image
    captcha_image_data_url = page.evaluate(
        """(captchaImageSelector) => {
            const img = document.querySelector(captchaImageSelector);
            return img.src;
        }""",
        captcha_image_selector,
    )

    # Decode the base64 image data
    image_data = base64.b64decode(captcha_image_data_url.split(",")[1])

    # Convert the image to grayscale using OpenCV (cv2)
    grayscale_image = cv2.cvtColor(
        cv2.imdecode(numpy.frombuffer(
            image_data, numpy.uint8), -1), cv2.COLOR_BGR2GRAY
    )

    # Perform OCR on the grayscale image
    captcha_text = pytesseract.image_to_string(
        Image.fromarray(grayscale_image))

    page.locator("#captcha").fill(captcha_text)
    time.sleep(4)
    page.locator("button[type='submit']").click()
    # page.locator("//form[2]").click()
    # time.sleep(30)
    # page.locator("//span[normalize-
    # space()='Text xxxxxxxx79']").click()
    # page.locator("//input[@id='code']").click()
    # time.sleep(15)
    # page.locator("button[type='submit']").click()
    page.screenshot(path="screenshot.png")
    # Print the CAPTCHA text
    print("Test CAPTCHA Text:", captcha_text)

    # Return the CAPTCHA text
    return captcha_text.strip()

    # time.sleep(4)


# print("Test CAPTCHA Text:", captcha_text)
