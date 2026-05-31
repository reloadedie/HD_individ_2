import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

url = "https://cbr.ru/hd_base/KeyRate/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

data = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) >= 2:
        date = cols[0].text.strip()
        rate = cols[1].text.strip().replace(',', '.')
        data.append({'date': date, 'key_rate': float(rate)})

df = pd.DataFrame(data)
df.to_csv('data/key_rate.csv', index=False)
print(f"Сохранено {len(df)} записей ключевой ставки")