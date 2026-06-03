import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

os.makedirs('data', exist_ok=True)

random.seed(42)
np.random.seed(42)

# 1. ХАРАКТЕРИСТИКИ АВТОМОБИЛЕЙ (на основе Auto.ru и Drom.ru)
cars = pd.DataFrame([
    {'brand': 'Lada', 'model': 'Vesta', 'engine_volume': 1.6, 'power_hp': 106, 'body_type': 'Sedan', 'drive': 'Front'},
    {'brand': 'Lada', 'model': 'Granta', 'engine_volume': 1.6, 'power_hp': 90, 'body_type': 'Sedan', 'drive': 'Front'},
    {'brand': 'Hyundai', 'model': 'Creta', 'engine_volume': 1.6, 'power_hp': 123, 'body_type': 'SUV', 'drive': 'Front'},
    {'brand': 'Kia', 'model': 'Rio', 'engine_volume': 1.6, 'power_hp': 100, 'body_type': 'Sedan', 'drive': 'Front'},
    {'brand': 'Toyota', 'model': 'RAV4', 'engine_volume': 2.0, 'power_hp': 146, 'body_type': 'SUV', 'drive': 'Full'},
    {'brand': 'Chery', 'model': 'Tiggo7', 'engine_volume': 1.5, 'power_hp': 147, 'body_type': 'SUV', 'drive': 'Front'},
    {'brand': 'Geely', 'model': 'Coolray', 'engine_volume': 1.5, 'power_hp': 147, 'body_type': 'SUV', 'drive': 'Front'},
    {'brand': 'BMW', 'model': 'X5', 'engine_volume': 3.0, 'power_hp': 249, 'body_type': 'SUV', 'drive': 'Full'},
    {'brand': 'Mercedes', 'model': 'E-Class', 'engine_volume': 2.0, 'power_hp': 194, 'body_type': 'Sedan', 'drive': 'Rear'},
    {'brand': 'Volkswagen', 'model': 'Polo', 'engine_volume': 1.6, 'power_hp': 110, 'body_type': 'Sedan', 'drive': 'Front'},
])

# 2. МАКРОЭКОНОМИКА (реальные данные + прогноз)
months = []
current = datetime(2022, 1, 1)
while current <= datetime(2026, 12, 31):
    months.append(current.strftime('%Y-%m'))
    current = current.replace(day=1) + timedelta(days=32)
    current = current.replace(day=1)

macro = []
key_rate_history = [7.5, 7.5, 8.5, 12.0, 13.0, 15.0, 16.0, 16.0, 16.0, 18.0, 19.0, 21.0, 21.0, 21.0, 20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0]
usd_history = [82.5, 85.0, 95.0, 100.0, 92.0, 88.0, 90.0, 88.0, 90.5, 85.0, 91.0, 96.0, 98.0, 105.0, 102.0, 99.0, 95.0, 92.0, 90.0, 88.0, 87.0, 86.0]

for i, month in enumerate(months):
    year = int(month.split('-')[0])
    idx = min(i, len(key_rate_history)-1)
    macro.append({
        'year_month': month,
        'key_rate': key_rate_history[idx] + (year - 2024) * -1.0,
        'usd_rub': usd_history[idx] + (year - 2024) * -1.5,
        'inflation_pct': max(0.3, 0.86 - (year - 2024) * 0.15)
    })

df_macro = pd.DataFrame(macro)

# 3. ПРОДАЖИ (симуляция с учетом утильсбора)
sales = []
for month in months:
    year = int(month.split('-')[0])
    for _, car in cars.iterrows():
        # Определяем категорию по объему двигателя
        if car['engine_volume'] <= 2.0:
            category = '0-2.0'
        elif car['engine_volume'] <= 3.0:
            category = '2.0-3.0'
        elif car['engine_volume'] <= 3.5:
            category = '3.0-3.5'
        else:
            category = '3.5+'
        
        # Утильсбор зависит от года
        if year <= 2023:
            util_fee = 34000
        elif year == 2024:
            util_fee = 44200
        elif year == 2025:
            util_fee = 50000
        elif year == 2026:
            util_fee = 57500
        else:
            util_fee = 66125
        
        # Базовая цена
        base_price = car.get('price', 1500000) if 'price' in car else 1500000
        price = base_price + util_fee * 1.5
        
        # Коэффициент продаж (зависит от цены, ставки, утильсбора)
        sales_coef = 1 - (price / 5000000) * 0.5
        sales_coef -= (df_macro[df_macro['year_month'] == month]['key_rate'].values[0] - 10) * 0.03
        
        qty = max(50, int(500 * sales_coef * random.uniform(0.8, 1.2)))
        
        sales.append({
            'year_month': month,
            'brand': car['brand'],
            'model': car['model'],
            'engine_volume': car['engine_volume'],
            'power_hp': car['power_hp'],
            'price_rub': int(price),
            'sales_qty': qty,
            'util_fee_rub': util_fee
        })

df_sales = pd.DataFrame(sales)

# 4. ОБЪЕДИНЯЕМ ВСЕ
df_final = df_sales.merge(df_macro, on='year_month', how='left')
df_final.to_csv('data/simulated_car_market_data.csv', index=False)

print(f"Создан файл: data/simulated_car_market_data.csv")
print(f"  Записей: {len(df_final)}")
print(f"  Колонки: {list(df_final.columns)}")
print(f"  Период: {df_final['year_month'].min()} - {df_final['year_month'].max()}")