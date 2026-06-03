import pandas as pd
import os

os.makedirs('data', exist_ok=True)

# Базовые ставки на 2025 год (из твоего файла)
base_2025 = {
    '0-2.0': 667440,
    '2.0-3.0': 1875600,
    '3.0-3.5': 2153400,
    '3.5+': 2742300,
}

# Коэффициенты индексации (на основе тренда из постановлений)
# 2025 → 2026: +15%
# 2026 → 2027: +15%
# 2027 → 2028: +15%

indexation = {
    2025: 1.00,
    2026: 1.15,
    2027: 1.32,  # 1.15 * 1.15
    2028: 1.52,  # 1.15 * 1.15 * 1.15
}

forecast_data = []
for year, coef in indexation.items():
    for category, base in base_2025.items():
        forecast_data.append({
            'year': year,
            'engine_category': category,
            'util_fee_rub': int(base * coef),
            'indexation_coefficient': coef,
            'change_pct': int((coef - 1) * 100),
            'source': 'forecast_based_on_2024_indexation_trend'
        })

df_forecast = pd.DataFrame(forecast_data)
df_forecast.to_csv('data/util_fee_forecast_2026_2028.csv', index=False)

print("ПРОГНОЗ УТИЛЬСБОРА НА 2026-2028:")
print(df_forecast.to_string(index=False))