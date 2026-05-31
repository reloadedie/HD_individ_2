import pandas as pd
import requests
import os
from io import BytesIO

os.makedirs('data', exist_ok=True)

url = "https://rosstat.gov.ru/storage/mediabank/3_06-02-2025.xlsx"
response = requests.get(url)
df = pd.read_excel(BytesIO(response.content), skiprows=4)

inflation_col = None
for col in df.columns:
    if 'инфляц' in str(col).lower() or 'ИПЦ' in str(col):
        inflation_col = col
        break

if inflation_col:
    result = df[['Месяц', inflation_col]].copy()
    result.columns = ['month', 'inflation_pct']
    result.to_csv('data/inflation.csv', index=False)
    print(f"Сохранено {len(result)} записей инфляции")