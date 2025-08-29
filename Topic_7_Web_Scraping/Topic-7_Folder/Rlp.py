from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver

# Setup browser
driver = webdriver.Chrome()
driver.get("https://open.rlp.de/de/suchergebnisse")
time.sleep(5)

# Parse HTML
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

# Get Panel 1 (index 0)
panels = soup.find_all('div', class_='accordion__panel')

if len(panels) > 0:
    panel = panels[0]  # Panel 1 is at index 0
    categories_text = panel.get_text(separator=' ')
    
    # Clean up the text
    clean_text = re.sub(r'\s+', ' ', categories_text).strip()
    clean_text = re.sub(r'Mehr anzeigen\s*Weniger anzeigen', '', clean_text, flags=re.IGNORECASE).strip()

    # Remove "Themen" if it appears at the beginning
    clean_text = re.sub(r'^Themen\s*', '', clean_text)

    # Insert newline after each closing parenthesis
    formatted_text = re.sub(r'\)\s*', r')\n', clean_text)

    # Remove dot from numbers inside parentheses (e.g., (1.234) → (1234))
    final_text = re.sub(r'\((\d+)\.(\d+)\)', r'(\1\2)', formatted_text)

    print(" Extracted Categories:\n")
    print(final_text)
else:
    print(" No accordion panels found.")

