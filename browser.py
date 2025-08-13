from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from pathlib import Path
from dotenv import load_dotenv

import os

load_dotenv()

ROOT_DIR = Path(__file__).parent
GECKODRIVER_NAME = "geckodriver"
GECKODRIVER_PATH = ROOT_DIR / "bin" / GECKODRIVER_NAME

print(f"Using geckodriver at: {GECKODRIVER_PATH}")


def make_firefox_browser(*options):
    firefox_options = webdriver.FirefoxOptions()

    if options is not None:
        for option in options:
            firefox_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == "1":
        firefox_options.add_argument("--headless")

    firefox_service = Service(executable_path=str(GECKODRIVER_PATH))
    browser = webdriver.Firefox(service=firefox_service, options=firefox_options)  # noqa

    return browser


if __name__ == '__main__':
    browser = make_firefox_browser('--headless')
    browser.get("https://www.youtube.com/")
    browser.quit()
