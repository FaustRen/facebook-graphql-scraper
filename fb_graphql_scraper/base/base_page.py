# -*- coding:utf-8 -*-
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service


class BasePage(object):
    def __init__(self, driver_path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        svc = Service(driver_path)
        self.driver = webdriver.Chrome(service=svc,options=chrome_options)
        self.driver.maximize_window()