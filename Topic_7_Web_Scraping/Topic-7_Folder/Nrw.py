from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Setup the browser
driver = webdriver.Chrome()

# Open the page
driver.get("https://open.nrw/suche?volltext=&page=1")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'select-categories'))
)


# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

# Extract categories
categories_panel = soup.find('div', id='select-categories')

if categories_panel:
    categories_text = categories_panel.get_text(separator=' ')

    # Clean and format text
    clean_text = re.sub(r'\s+', ' ', categories_text).strip()

    # Remove "Kategorien" if it appears at the beginning
    clean_text = re.sub(r'^Kategorien\s*', '', clean_text)

    # Insert newline after each digit sequence (count)
    final_text = re.sub(r'(\d+)\s+', r'\1\n', clean_text)

    # Remove unwanted trailing text
    final_text = re.sub(r'(Alle anzeigen.*)', '', final_text).strip()

    print(final_text)
else:
    print("Category panel not found.")