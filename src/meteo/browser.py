"""Headless Firefox driver setup.

Only Firefox/geckodriver is actually used anywhere in this project -- the
old repo also carried a `chromedriver.exe` binary and a `chromedriver-py`
dependency that no scraper ever touched. Dropped in v2.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@contextmanager
def firefox_driver(headless: bool = True) -> Iterator[webdriver.Firefox]:
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    try:
        yield driver
    finally:
        driver.quit()
