import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

url = "https://www.investing.com/currencies/usd-rub-historical-data"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'historicalTbl'})
data = []

if table:
    rows = table.find_all('tr')[1:31]
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 6:
            date = cols[0].text.strip()
            price = cols[1].text.strip().replace(',', '')
            data.append({
                'date': date,
                'usd_rub': float(price),
                'open': cols[2].text.strip(),
                'high': cols[3].text.strip(),
                'low': cols[4].text.strip()
            })

df = pd.DataFrame(data)
df.to_csv('data/investing_usd.csv', index=False)
print(f"Сохранено {len(df)} записей курса с investing.com")