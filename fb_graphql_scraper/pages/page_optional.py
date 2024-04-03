# -*- coding: utf-8 -*-
from fb_graphql_scraper.utils.locator import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class PageOptional(object):
    def __init__(self, url_in: str, driver=None, fb_account: str = None, pwd: str = None):
        self.locator = PageLocators
        self.xpath_elements = PageXpath
        self.class_elements = PageClass
        self.page_text = PageText
        self.driver = driver
        self.url = url_in
        self.driver.get(url=self.url)
        self.fb_account = fb_account
        self.pwd = pwd
        time.sleep(3)

        # Loggin account
        if self.fb_account and self.pwd:
            self.login_page()

        # 免登入帳號, 適用不需登入帳號的爬蟲目標 / Without logging, click X button
        else:
            self.click_reject_login_button()

    def login_page(self):
        try:
            self.login_account(user=self.fb_account, password=self.pwd,
                               user_element=self.locator.LOGGINUSR1, pwd_element=self.locator.LOGGINPWD1)
        except:
            self.login_account(user=self.fb_account, password=self.pwd,
                               user_element=self.locator.LOGGINUSR2, pwd_element=self.locator.LOGGINPWD2)

    def clean_requests(self):
        try:
            print("Try to clear driver requests..")
            del self.driver.requests
            print("Clear")
        except Exception as e:
            print(f"Clear unsuccessfully, message: {e}")

    def get_in_url(self):
        self.driver.get(url=self.url)

    def login_account(self, user: str, password: str, user_element, pwd_element):
        user_element = self.driver.find_element(By.XPATH, user_element)
        user_element.send_keys(user)
        password_element = self.driver.find_element(By.XPATH, pwd_element)
        password_element.send_keys(password)
        password_element.send_keys(Keys.ENTER)

    def scroll_window(self):
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")

    def scroll_window_with_parameter(self, parameter_in: str):
        self.driver.execute_script(f"window.scrollBy(0, {parameter_in});")

    def set_browser_zoom_percent(self, zoom_percent: int):
        zoom_percent = str(zoom_percent)
        self.driver.execute_script(
            f"document.body.style.zoom='{zoom_percent}%'")

    def move_to_element(self, element_in):
        ActionChains(self.driver).move_to_element(element_in).perform()

    def click_display_button(self):
        elements = self.driver.find_elements(self.locator.DISPLAY_MORE)
        for _ in range(10):
            for each_element in elements:
                if each_element.text == self.page_text.DISPLAY_MORE or each_element.text == self.page_text.DISPLAY_MORE2:
                    self.move_to_element(element_in=each_element)
                    self.scroll_window_with_parameter(parameter_in="500")
                    try:
                        each_element.click()
                        elements = self.driver.find_elements(
                            self.locator.DISPLAY_MORE)
                    except Exception as e:
                        print(
                            f"Click display more unsucessfully, error message:\n{e}")

    def click_display_button2(self):
        display_more_xpath = f"//div[@class='{PageClass.DISPLAY_MORE}' and @role='{PageRoleValue.DISPLAY_MORE}' and text()='{PageText.DISPLAY_MORE}']"
        elements = self.driver.find_elements(By.XPATH, display_more_xpath)
        for _ in range(10):
            for each_element in elements:
                if each_element.text == self.page_text.DISPLAY_MORE or each_element.text == self.page_text.DISPLAY_MORE2:
                    self.move_to_element(element_in=each_element)
                    self.scroll_window_with_parameter(parameter_in="500")
                    try:
                        each_element.click()
                        elements = self.driver.find_elements(
                            self.locator.DISPLAY_MORE)
                    except Exception as e:
                        print(
                            f"Click display more unsucessfully, error message:\n{e}")

    def click_reject_login_button(self):
        try:
            reject_login_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((self.locator.CLOSELOGIN)))
            reject_login_button.click()
        except Exception as e:
            print(f"Click reject button failed, message:{e}")

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()
