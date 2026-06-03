import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

os.makedirs('data', exist_ok=True)

url = "https://aebrus.ru/statistics/sales/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

excel_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if '.xlsx' in href.lower() or '.xls' in href.lower():
        if 'car' in href.lower() or 'sales' in href.lower() or '2024' in href or '2025' in href:
            if href.startswith('/'):
                excel_links.append('https://aebrus.ru' + href)
            else:
                excel_links.append(href)

all_sales = []
for link in excel_links[:5]:
    try:
        df_temp = pd.read_excel(link, engine='openpyxl')
        all_sales.append(df_temp)
        print(f"Загружен: {link.split('/')[-1]}")
    except:
        try:
            df_temp = pd.read_excel(link)
            all_sales.append(df_temp)
            print(f"Загружен: {link.split('/')[-1]}")
        except:
            pass

if all_sales:
    df = pd.concat(all_sales, ignore_index=True)
    df.to_csv('data/aeb_sales.csv', index=False)
    print(f"Сохранено {len(df)} записей продаж АЕБ")
else:
    print("Не удалось загрузить файлы АЕБ, создаю структуру")
    empty_df = pd.DataFrame(columns=['year_month', 'brand', 'model', 'sales_qty'])
    empty_df.to_csv('data/aeb_sales.csv', index=False)