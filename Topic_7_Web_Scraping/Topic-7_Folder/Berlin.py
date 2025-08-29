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
driver.get("https://daten.berlin.de/datensaetze") 
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'facet_dp_facet_groups'))
)

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

# Extract categories
categories_panel = soup.find('div', id='facet_dp_facet_groups')
if categories_panel:
    text = categories_panel.get_text(" ", strip=True)
    text = re.sub(r'\s+', ' ', text)                        # Normalize spaces
    text = re.sub(r'\(\d+\)', lambda m: f"{m.group()}\n", text)  # Newline after counts
    text = re.sub(r'Mehr anzeigen.*', '', text, flags=re.IGNORECASE)  # Remove trailing
    lines = text.strip().split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    print('\n'.join(clean_lines))
else:
    print("Category panel not found.")