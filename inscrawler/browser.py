import os
from selenium import webdriver
from selenium.webdriver.common.by import By


class Browser:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        service_args = ['--ignore-ssl-errors=true']
        self.driver = webdriver.PhantomJS(
            executable_path='%s/bin/phantomjs' % dir_path,
            service_args=service_args)
        self.driver.implicitly_wait(5)

    def get(self, url):
        self.driver.get(url)

    def find_one(self, css_selector, elem=None):
        obj = elem or self.driver
        return obj.find_element(By.CSS_SELECTOR, css_selector)

    def find(self, css_selector, elem=None):
        obj = elem or self.driver
        return obj.find_elements(By.CSS_SELECTOR, css_selector)

    def scroll_down(self):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')

    def scroll_up(self):
        self.driver.execute_script(
            'window.scrollTo(0, 0)')

    def __del__(self):
        self.driver.quit()
