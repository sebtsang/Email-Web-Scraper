from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import time

# Initialise chrome driver
driver = webdriver.Chrome()
url = "https://www.parksattexasstar.com/softball/free-agents"
driver.get(url)

# Go to contact page
contactPage = driver.find_element("xpath", '//a[contains(text(), "Contact")]')
contactPage.click()

email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
html = driver.page_source
emails = re.findall(email_pattern, html)

matches = driver.find_elements(By.TAG_NAME, 'tr')

name = []
role = []
email = []

time.sleep(5)
for i, email in enumerate(emails):
    print(f'{i + 1}: {email}')
for match in matches:
    print(match.text)
driver.close()
