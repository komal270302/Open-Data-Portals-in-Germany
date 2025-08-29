from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the browser
driver = webdriver.Chrome()
url = 'https://www.govdata.de/suche?q=hessen'
driver.get(url)

try:
    # Wait for the category section
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "details:nth-child(2) > div"))
    )

    # Find the category filter block
    category_div = driver.find_element(By.CSS_SELECTOR, "details:nth-child(2) > div")
    category_elements = category_div.find_elements(By.CSS_SELECTOR, ".gd-filterarea-link")

    seen = set()

    # Loop and print only unique categories with counts
    for category in category_elements:
        title = category.find_element(By.CLASS_NAME, "gd-filterarea-link-title").text.strip()
        count = category.find_element(By.CLASS_NAME, "gd-badge").text.strip()

        # Remove newlines and ensure clean format
        title_clean = title.replace('\n', ' ')
        count_clean = count.replace('\n', '').replace('Treffer', '').strip()


        if title_clean not in seen:
            seen.add(title_clean)
            print(f"{title_clean} ({count_clean})")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()      
