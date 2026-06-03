import pandas as pd
import os

os.makedirs('data', exist_ok=True)

# РЕАЛЬНЫЕ СТАВКИ УТИЛЬСБОРА (из постановлений)
util_fee_real = pd.DataFrame([
    # ПОСТАНОВЛЕНИЕ №1255 от 13.09.2024
    {'date': '2024-10-01', 'engine_volume_min': 0, 'engine_volume_max': 2.0,
     'util_fee_rub': 556200, 'source': 'Постановление №1255', 'year': 2024},
    {'date': '2024-10-01', 'engine_volume_min': 2.0, 'engine_volume_max': 3.0,
     'util_fee_rub': 1563000, 'source': 'Постановление №1255', 'year': 2024},
    {'date': '2024-10-01', 'engine_volume_min': 3.0, 'engine_volume_max': 3.5,
     'util_fee_rub': 1794600, 'source': 'Постановление №1255', 'year': 2024},
    {'date': '2024-10-01', 'engine_volume_min': 3.5, 'engine_volume_max': 10.0,
     'util_fee_rub': 2284000, 'source': 'Постановление №1255', 'year': 2024},

    # ПЛАНИРУЕМЫЕ СТАВКИ С 01.01.2025
    {'date': '2025-01-01', 'engine_volume_min': 0, 'engine_volume_max': 2.0,
     'util_fee_rub': 667440, 'source': 'Постановление №1255 (план)', 'year': 2025},
    {'date': '2025-01-01', 'engine_volume_min': 2.0, 'engine_volume_max': 3.0,
     'util_fee_rub': 1875600, 'source': 'Постановление №1255 (план)', 'year': 2025},
    {'date': '2025-01-01', 'engine_volume_min': 3.0, 'engine_volume_max': 3.5,
     'util_fee_rub': 2153400, 'source': 'Постановление №1255 (план)', 'year': 2025},
    {'date': '2025-01-01', 'engine_volume_min': 3.5, 'engine_volume_max': 10.0,
     'util_fee_rub': 2742300, 'source': 'Постановление №1255 (план)', 'year': 2025},
])

util_fee_real.to_csv('data/util_fee_real.csv', index=False)
print("Сохранены реальные ставки утильсбора")
print(util_fee_real)