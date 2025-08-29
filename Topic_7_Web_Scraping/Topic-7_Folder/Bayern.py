from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Setup driver
options = Options()
driver = webdriver.Chrome(
    service=Service(r"C:\Users\Dell\Desktop\chromedriver-win64\chromedriver.exe"),
    options=options
)

driver.get("https://open.bydata.de/datasets?locale=de&page=1&limit=10")

# Wait for category panel
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'facet-list-categories'))
)

# Click "Mehr anzeigen"
try:
    expand_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#facet-list-categories > button'))
    )
    driver.execute_script("arguments[0].click();", expand_button)
    time.sleep(2)
    print(" 'Mehr anzeigen' clicked.")
except Exception as e:
    print(" Could not click 'Mehr anzeigen':", e)

# Scroll panel slowly to trigger rendering
try:
    panel = driver.find_element(By.ID, "facet-list-categories")
    for i in range(0, 1000, 50):  # simulate smooth scroll
        driver.execute_script("arguments[0].scrollTop = arguments[1];", panel, i)
        time.sleep(0.3)
    print(" Smooth scroll complete.")
except Exception as e:
    print(" Scrolling failed:", e)

# Extract visible category labels using Selenium directly
try:
    element = driver.find_element(By.ID, "facet-list-categories")
    lines = [line.strip() for line in element.text.strip().split('\n') if line.lower() != "expand_less"]

    i = 0
    while i < len(lines) - 1:
        category = lines[i]
        number = lines[i + 1].replace(' ', '').replace('.', '')
        if number.isdigit():
            print(f"{category} ({number})")
            i += 2
        else:
            i += 1

except Exception as e:
    print("Failed to extract category labels:", e)

driver.quit()








