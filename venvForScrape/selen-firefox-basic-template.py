from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui


service = Service(executable_path="/snap/bin/geckodriver")
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=options)

driver.get('https://www.google.com/')
page_url=driver.find_elements("xpath","/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[2]")
#all_title = driver.find_elements_by_class_name("title")
#title = [title.text for title in all_title]
print(page_url)