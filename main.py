import subprocess
import sys
import os
import pandas as pd

os.makedirs('data', exist_ok=True)


def check_and_install_packages():
    packages = ['pandas', 'requests', 'beautifulsoup4', 'playwright', 'openpyxl']
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def run_parser_script(filepath):
    if not os.path.exists(filepath):
        print(f"[ОШИБКА] {filepath} не найден")
        return False

    print(f"\n{'=' * 70}")
    print(f"ВЫПОЛНЕНИЕ: {filepath}")
    print('=' * 70)

    try:
        result = subprocess.run([sys.executable, filepath], capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"[ОШИБКА] {filepath}: {e}")
        return False


def run_async_parser(filepath):
    if not os.path.exists(filepath):
        print(f"[ОШИБКА] {filepath} не найден")
        return False

    print(f"\n{'=' * 70}")
    print(f"ВЫПОЛНЕНИЕ: {filepath}")
    print('=' * 70)

    try:
        result = subprocess.run([sys.executable, filepath], capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"[ОШИБКА] {filepath}: {e}")
        return False


def run_util_fee_parser():
    print("\n" + "=" * 70)
    print("ВЫПОЛНЕНИЕ: util_fee_indexation.py (из папки util_sbor)")
    print("=" * 70)

    util_file_path = "util_sbor/util_fee_indexation.py"
    if not os.path.exists(util_file_path):
        print(f"[ОШИБКА] {util_file_path} не найден")
        return False

    try:
        subprocess.run([sys.executable, util_file_path], capture_output=False)
        return True
    except Exception as e:
        print(f"[ОШИБКА] {util_file_path}: {e}")
        return False


def run_simulation():
    print("\n" + "=" * 70)
    print("ЗАПУСК СИМУЛЯЦИИ ДАННЫХ")
    print("=" * 70)

    if os.path.exists("simulate_data_for_loginom.py"):
        subprocess.run([sys.executable, "simulate_data_for_loginom.py"], capture_output=False)
    else:
        print("Файл simulate_data_for_loginom.py не найден")


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
        try:
            df = pd.read_csv(filepath)
            summary_data.append({
                'Файл': f,
                'Строк': len(df),
                'Столбцов': len(df.columns),
                'Размер (КБ)': round(os.path.getsize(filepath) / 1024, 1)
            })
        except:
            pass

    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))

    print("\n" + "-" * 70)
    print("ГЛАВНЫЙ ФАЙЛ ДЛЯ LOGINOM: data/simulated_car_market_data.csv")
    print("-" * 70)


def orchestrate():
    print("=" * 70)
    print("ПАРСИНГ ДАННЫХ ДЛЯ ХД 'РЫНОК НОВЫХ АВТОМОБИЛЕЙ'")
    print("=" * 70)

    check_and_install_packages()

    # Работающие парсеры
    results = {}

    results['cbr_key_rate_parser.py'] = run_parser_script("cbr_key_rate_parser.py")
    results['cbr_usd_parser.py'] = run_parser_script("cbr_usd_parser.py")

    # Playwright парсеры (Auto.ru и Drom.ru)
    results['auto_ru_parser.py'] = run_async_parser("auto_ru_parser.py")
    results['drom_ru_parser.py'] = run_async_parser("drom_ru_parser.py")

    # Утильсбор и симуляция
    results['util_fee_indexation.py'] = run_util_fee_parser()
    run_simulation()

    show_summary()

    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ")
    print("=" * 70)
    for parser, success in results.items():
        status = "УСПЕХ" if success else "ОШИБКА"
        print(f"{status:10} | {parser}")


if __name__ == "__main__":
    orchestrate()