import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

url = "https://www.cbr.ru/currency_base/daily/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

data = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) >= 5 and 'USD' in cols[1].text:
        date = cols[0].text.strip()
        rate = cols[4].text.strip().replace(',', '.')
        data.append({'date': date, 'usd_rub': float(rate)})

df = pd.DataFrame(data)
df.to_csv('data/usd_rate.csv', index=False)
print(f"Сохранено {len(df)} записей курса USD")