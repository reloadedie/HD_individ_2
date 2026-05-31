from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
import os

os.makedirs('data', exist_ok=True)

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

url = "https://www.drom.ru/catalog/all/"
driver.get(url)

time.sleep(5)

cars = []
brands = driver.find_elements(By.CSS_SELECTOR, '[data-ftid="component_brand"]')

for brand in brands[:10]:
    try:
        brand_name = brand.text
        brand.click()
        time.sleep(2)

        models = driver.find_elements(By.CSS_SELECTOR, '[data-ftid="component_model"]')
        for model in models[:5]:
            try:
                model_name = model.text
                model.click()
                time.sleep(2)

                listings = driver.find_elements(By.CSS_SELECTOR, '[data-ftid="bull_list_item"]')
                for listing in listings[:3]:
                    try:
                        price_elem = listing.find_element(By.CSS_SELECTOR, '[data-ftid="bull_price"]')
                        price = re.sub(r'[^\d]', '', price_elem.text)

                        specs = listing.find_elements(By.CSS_SELECTOR, '[data-ftid="bull_specs"]')
                        specs_text = specs[0].text if specs else ''

                        cars.append({
                            'brand': brand_name,
                            'model': model_name,
                            'price_rub': int(price) if price else None,
                            'specs': specs_text
                        })
                    except:
                        pass

                driver.back()
                time.sleep(1)
            except:
                pass

        driver.get(url)
        time.sleep(2)
    except:
        pass

driver.quit()

df = pd.DataFrame(cars)
df.to_csv('data/drom_cars.csv', index=False)
print(f"Сохранено {len(df)} записей автомобилей")