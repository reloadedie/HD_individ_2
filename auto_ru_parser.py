from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

os.makedirs('data', exist_ok=True)

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

url = "https://auto.ru/cars/new/all/"
driver.get(url)

time.sleep(5)

cars = []
last_height = driver.execute_script("return document.body.scrollHeight")
while len(cars) < 200:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    cards = driver.find_elements(By.CLASS_NAME, 'ListingItem')
    for card in cards:
        try:
            name = card.find_element(By.CLASS_NAME, 'ListingItemTitle').text
            price = card.find_element(By.CLASS_NAME, 'ListingItemPrice').text
            price = re.sub(r'[^\d]', '', price)

            tech = card.find_elements(By.CLASS_NAME, 'ListingItemTechSummary')
            tech_text = tech[0].text if tech else ''

            engine = re.search(r'(\d+\.?\d*)\s*л', tech_text)
            power = re.search(r'(\d+)\s*л\.с', tech_text)

            cars.append({
                'name': name,
                'price_rub': int(price) if price else None,
                'engine_volume_l': float(engine.group(1)) if engine else None,
                'power_hp': int(power.group(1)) if power else None,
                'full_text': tech_text
            })
        except:
            pass

driver.quit()

df = pd.DataFrame(cars)
df.to_csv('data/auto_ru_cars.csv', index=False)
print(f"Сохранено {len(df)} записей автомобилей")