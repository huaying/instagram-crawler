from selenium import webdriver
from selenium.webdriver.common.by import By
from browsermobproxy import Server


class Browser:
    def __init__(self):
        self.server = Server("./browsermob-proxy")
        self.server.start()
        self.proxy = self.server.create_proxy()
        service_args = [
            '--proxy={0}'.format(self.proxy.proxy), '--ignore-ssl-errors=true']
        self.driver = webdriver.PhantomJS(service_args=service_args)
        self.driver.implicitly_wait(5)

    def get(self, url):
        self.driver.get(url)

    def find_one(self, css_selector):
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def find(self, css_selector):
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)

    def requests_listen(self, name):
        self.proxy.new_har(name)

    def requests(self):
        return [
            entry['request']['url']
            for entry in self.proxy.har['log']['entries']
        ]

    def __del__(self):
        self.server.stop()
        self.driver.quit()
