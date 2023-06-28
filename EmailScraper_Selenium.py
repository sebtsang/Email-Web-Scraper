from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import time

url = input("Enter the URL of the website you want to scrape: ")

# Check if the URL contains "http://" or "https://", add if missing
if not url.startswith("http://") and not url.startswith("https://"):
    url = "http://" + url

# Extract the domain from the URL
match = re.search(r"(.*?)(?=.com)", url)
if match:
    domain = match.group()
else:
    print("Invalid URL format. Please make sure the URL contains '.com'")
    exit()

# Initialise chrome driver
driver = webdriver.Chrome()
driver.get(url)

# Find all the anchor elements on the page
links = driver.find_elements(By.TAG_NAME, 'a')

# Collect the href attribute and anchor text from each anchor element
page_list = [(element.get_attribute('href'), element.get_attribute('innerText')) for element in links]

# Filter the page list to remove any None values and non-matching domains
page_list = [(href, text) for href, text in page_list if href is not None and domain in href and ".com" in href]

print(page_list)

print(len(page_list), "pages found \n")

# Define email pattern
email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"

# Loop through each page in the page_list
for href, anchor_text in page_list:
    # Navigate to the page
    driver.get(href)

    # Wait for a few seconds to ensure the page is fully loaded
    time.sleep(2)

    # Scrape the email addresses using the defined pattern
    html = driver.page_source
    page_emails = re.findall(email_pattern, html)

    # Skip the page if no emails found
    if not page_emails:
        continue

    # Create empty lists for storing scraped data
    emails = []
    names = []
    roles = []

    # Append the scraped emails to the main list
    emails.extend(page_emails)

    # Scrape the table rows (assuming the table rows contain name and role)
    table_rows = driver.find_elements(By.TAG_NAME, 'tr')

    # Extract the name and role from each table row and append them to respective lists
    for row in table_rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) >= 2:
            name = cells[0].text
            role = cells[1].text
            names.append(name)
            roles.append(role)

    # Print the scraped emails, names, and roles for the current page
    for i, email in enumerate(emails):
        if i < len(names) and i < len(roles):
            name = names[i]
            role = roles[i]
            print(f'Email: {email}, Name: {name}, Role: {role}, Page: {anchor_text}', href)
        else:
            print(f'Email: {email}, Name: N/A, Role: N/A (No corresponding name and role data), Page: {anchor_text}')

    print()  # Add a new line between pages

# Close the browser
driver.close()