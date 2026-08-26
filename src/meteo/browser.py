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
# the following import is commented out because it downloads a new geckodriver binary every time, which is slow and unnecessary.
# from webdriver_manager.firefox import GeckoDriverManager


@contextmanager
def firefox_driver(headless: bool = True) -> Iterator[webdriver.Firefox]:
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    # this uses the geckodriver binary installed by webdriver-manager, which is a
    # different binary than the one that comes with Firefox itself. The latter is
    # not used anywhere in this project.
    ## driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    # the above line is commented out because it downloads a new geckodriver binary every time, which is slow and unnecessary.
    #  Instead, we rely on the geckodriver binary that comes with Firefox itself, which is already installed on the system.
    driver = webdriver.Firefox(service=FirefoxService(), options=options)


    try:
        yield driver
    finally:
        driver.quit()
