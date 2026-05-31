import subprocess
import sys
import os
import pandas as pd
import importlib.util


def check_and_install_packages():
    packages = ['pandas', 'requests', 'beautifulsoup4', 'selenium', 'openpyxl', 'lxml']
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])


def run_parser_file(filepath):
    if not os.path.exists(filepath):
        print(f"[ОШИБКА] {filepath} не найден")
        return False

    print(f"\n{'=' * 70}")
    print(f"ВЫПОЛНЕНИЕ: {filepath}")
    print('=' * 70)

    try:
        spec = importlib.util.spec_from_file_location("parser", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True
    except Exception as e:
        print(f"[ОШИБКА] {filepath}: {e}")
        return False


def show_summary():
    print("\n" + "=" * 70)
    print("ИТОГОВЫЙ ОТЧЕТ О СОБРАННЫХ ДАННЫХ")
    print("=" * 70)

    if not os.path.exists('data'):
        print("Папка 'data' не создана")
        return

    files = sorted([f for f in os.listdir('data') if f.endswith('.csv')])

    if not files:
        print("CSV файлы не найдены")
        return

    summary_data = []
    for f in files:
        filepath = os.path.join('data', f)
        df = pd.read_csv(filepath)
        summary_data.append({
            'Файл': f,
            'Строк': len(df),
            'Столбцов': len(df.columns),
            'Размер (КБ)': round(os.path.getsize(filepath) / 1024, 1)
        })

    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))

    print("\n" + "-" * 70)
    print("ГОТОВО К ЗАГРУЗКЕ В LOGINOM")
    print("Файлы находятся в папке: ./data/")
    print("-" * 70)


def orchestrate():
    print("=" * 70)
    print("ОРКЕСТРАЦИЯ ПАРСИНГА ДАННЫХ ДЛЯ ХД 'РЫНОК НОВЫХ АВТОМОБИЛЕЙ'")
    print("=" * 70)

    check_and_install_packages()

    parser_files = [
        "parser_1_key_rate.py",
        "parser_2_usd_rate.py",
        "parser_3_inflation.py",
        "parser_4_aeb_sales.py",
        "parser_5_auto_ru.py",
        "parser_6_drom_ru.py",
        "parser_7_investing.py"
    ]

    results = {}
    for parser_file in parser_files:
        success = run_parser_file(parser_file)
        results[parser_file] = success

    show_summary()

    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ")
    print("=" * 70)
    for parser, success in results.items():
        status = "✓ УСПЕХ" if success else "✗ ОШИБКА"
        print(f"{status:10} | {parser}")


if __name__ == "__main__":
    orchestrate()