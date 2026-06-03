import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

url = "https://www.investing.com/currencies/usd-rub-historical-data"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'historicalTbl'})
    if not table:
        table = soup.find('table', {'class': 'freeze-column'})

    data = []

    if table:
        rows = table.find_all('tr')[1:31]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 6:
                date = cols[0].text.strip()
                price = cols[1].text.strip().replace(',', '')
                try:
                    data.append({
                        'date': date,
                        'usd_rub': float(price),
                    })
                except:
                    pass

    if data:
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(columns=['date', 'usd_rub'])

    df.to_csv('data/investing_usd.csv', index=False)
    print(f"Сохранено {len(df)} записей с Investing.com")

except Exception as e:
    print(f"Ошибка парсинга Investing.com: {e}")
    empty_df = pd.DataFrame(columns=['date', 'usd_rub'])
    empty_df.to_csv('data/investing_usd.csv', index=False)