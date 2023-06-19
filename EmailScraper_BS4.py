from bs4 import BeautifulSoup
import requests
import re


urls = ['https://www.parksattexasstar.com/facilities/contact-us']
email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"

for url in urls:
    try:
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser')
        emails = re.findall(email_regex, doc.text)
        for i, email in enumerate(emails):
            print(f'{i + 1}: {email}')
    except requests.exceptions.RequestException as e:
        print(f"Error scraping website {url}: {e}")
