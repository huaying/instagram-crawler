import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep


class Browser:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        service_args = ['--ignore-ssl-errors=true']
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path='%s/bin/chromedriver' % dir_path,
            service_args=service_args,
            chrome_options=chrome_options)
        self.driver.implicitly_wait(5)

    @property
    def page_height(self):
        return self.driver.execute_script('return document.body.scrollHeight')

    def get(self, url):
        self.driver.get(url)

    def find_one(self, css_selector, elem=None):
        obj = elem or self.driver
        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find(self, css_selector, elem=None):
        obj = elem or self.driver
        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def scroll_down(self, wait=0.5):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')
        sleep(wait)

    def scroll_up(self, wait=2):
        self.driver.execute_script(
            'window.scrollTo(0, 0)')
        sleep(wait)

    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass
