import pandas as pd
import requests
import os
from io import BytesIO
import ssl

os.makedirs('data', exist_ok=True)

ssl._create_default_https_context = ssl._create_unverified_context

# Альтернативный URL с данными по инфляции (официальный сайт Росстата)
urls = [
    "https://rosstat.gov.ru/storage/mediabank/3_03-06-2025.xlsx",
    "https://rosstat.gov.ru/storage/mediabank/3_06-02-2025.xlsx",
    "https://rosstat.gov.ru/storage/mediabank/3_05-06-2025.xlsx",
]

df = None
for url in urls:
    try:
        response = requests.get(url, verify=False, timeout=30)

        # Проверяем, что вернулся именно Excel файл
        content_type = response.headers.get('Content-Type', '')
        if 'excel' in content_type.lower() or 'application/vnd' in content_type.lower() or response.content[
                                                                                           :4] == b'PK\x03\x04':
            df = pd.read_excel(BytesIO(response.content), skiprows=4, engine='openpyxl')
            print(f"Загружен файл: {url}")
            break
    except:
        continue

if df is not None:
    inflation_col = None
    month_col = None

    for col in df.columns:
        col_lower = str(col).lower()
        if 'инфляц' in col_lower or 'ипц' in col_lower:
            inflation_col = col
        if 'месяц' in col_lower or 'период' in col_lower:
            month_col = col

    if inflation_col and month_col:
        result = df[[month_col, inflation_col]].copy()
        result.columns = ['month', 'inflation_pct']
        result = result.dropna()
        result.to_csv('data/inflation.csv', index=False)
        print(f"Сохранено {len(result)} записей инфляции")
    else:
        print("ОШИБКА: Не найдены колонки")
else:
    print("ОШИБКА: Не удалось загрузить файл с Росстата")