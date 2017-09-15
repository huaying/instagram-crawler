from selenium import webdriver
from selenium.webdriver.common.by import By
from browsermobproxy import Server
server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

service_args = [
    '--proxy={0}'.format(proxy.proxy), '--ignore-ssl-errors=true']
driver = webdriver.PhantomJS(service_args=service_args)
driver.implicitly_wait(5)
driver.get('https://www.instagram.com/cal_foodie/')


a = driver.find_element(By.CSS_SELECTOR, '._kc4z2')
print(a)
loadmore_btn = driver.find_element(By.CSS_SELECTOR, '._1cr2e._epyes')
proxy.new_har("loadmore_click")
loadmore_btn.click()
all_requests = [
    entry['request']['url'] for entry in proxy.har['log']['entries']]

print(all_requests)

server.stop()
driver.quit()
