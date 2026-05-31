import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

os.makedirs('data', exist_ok=True)

url = "https://aebrus.ru/statistics/sales/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all('a', href=True)
excel_links = []
for link in links:
    if '.xlsx' in link['href'] and ('cars' in link['href'].lower() or 'sales' in link['href'].lower()):
        excel_links.append(link['href'])

data = []
for link in excel_links[:3]:
    if not link.startswith('http'):
        link = 'https://aebrus.ru' + link
    try:
        df_temp = pd.read_excel(link)
        data.append(df_temp)
    except:
        pass

if data:
    df = pd.concat(data, ignore_index=True)
    df.to_csv('data/aeb_sales.csv', index=False)
    print(f"Сохранено {len(df)} записей продаж")