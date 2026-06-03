import asyncio
import re
import pandas as pd
import os
from playwright.async_api import async_playwright

os.makedirs('data', exist_ok=True)


async def parse_auto_ru():
    cars = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        url = "https://auto.ru/cars/new/all/"
        await page.goto(url)
        await page.wait_for_timeout(5000)

        # Скроллим для загрузки
        for _ in range(5):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)

        # Ищем карточки
        cards = await page.query_selector_all('.ListingItem')

        for card in cards:
            try:
                # Название
                name_elem = await card.query_selector('.ListingItemTitle')
                name = await name_elem.inner_text() if name_elem else ''

                # Цена
                price_elem = await card.query_selector('.ListingItemPrice')
                price_text = await price_elem.inner_text() if price_elem else ''
                price = re.sub(r'[^\d]', '', price_text)

                # Характеристики
                tech_elem = await card.query_selector('.ListingItemTechSummary')
                tech_text = await tech_elem.inner_text() if tech_elem else ''

                engine = re.search(r'(\d+\.?\d*)\s*л', tech_text)
                power = re.search(r'(\d+)\s*л\.с', tech_text)

                brand = name.split()[0] if name else ''

                cars.append({
                    'brand': brand,
                    'full_name': name,
                    'price_rub': int(price) if price else None,
                    'engine_volume_l': float(engine.group(1)) if engine else None,
                    'power_hp': int(power.group(1)) if power else None,
                    'specs': tech_text
                })
            except Exception as e:
                continue

        await browser.close()

    return pd.DataFrame(cars)


async def main():
    df = await parse_auto_ru()
    df.to_csv('data/auto_ru_cars.csv', index=False)
    print(f"Сохранено {len(df)} записей с Auto.ru")


if __name__ == "__main__":
    asyncio.run(main())