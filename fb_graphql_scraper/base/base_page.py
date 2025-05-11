# -*- coding:utf-8 -*-
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

class BasePage:
    def __init__(self, driver_path: str, open_browser: bool = False):
        chrome_options = self._build_options(open_browser)
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()

    @staticmethod
    def _build_options(open_browser: bool) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if not open_browser:
            options.add_argument("--headless=new")
        options.add_argument("--blink-settings=imagesEnabled=false")
        return options
