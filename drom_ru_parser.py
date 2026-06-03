import asyncio
import re
import pandas as pd
import os
from playwright.async_api import async_playwright

os.makedirs('data', exist_ok=True)


async def parse_drom_ru():
    cars = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        url = "https://www.drom.ru/catalog/all/"
        await page.goto(url)
        await page.wait_for_timeout(5000)

        brands = await page.query_selector_all('[data-ftid="component_brand"]')

        for brand in brands[:5]:
            try:
                brand_name = await brand.inner_text()
                await brand.click()
                await page.wait_for_timeout(2000)

                models = await page.query_selector_all('[data-ftid="component_model"]')
                for model in models[:3]:
                    try:
                        model_name = await model.inner_text()
                        await model.click()
                        await page.wait_for_timeout(2000)

                        listings = await page.query_selector_all('[data-ftid="bull_list_item"]')
                        for listing in listings[:3]:
                            try:
                                price_elem = await listing.query_selector('[data-ftid="bull_price"]')
                                price_text = await price_elem.inner_text() if price_elem else ''
                                price = re.sub(r'[^\d]', '', price_text)

                                specs_elem = await listing.query_selector('[data-ftid="bull_specs"]')
                                specs_text = await specs_elem.inner_text() if specs_elem else ''

                                engine = re.search(r'(\d+\.?\d*)\s*л', specs_text)
                                power = re.search(r'(\d+)\s*л\.с', specs_text)

                                cars.append({
                                    'brand': brand_name,
                                    'model': model_name,
                                    'price_rub': int(price) if price else None,
                                    'engine_volume_l': float(engine.group(1)) if engine else None,
                                    'power_hp': int(power.group(1)) if power else None,
                                    'specs': specs_text[:200]
                                })
                            except Exception:
                                pass

                        await page.go_back()
                        await page.wait_for_timeout(1500)
                    except Exception:
                        pass

                await page.goto(url)
                await page.wait_for_timeout(2000)
            except Exception:
                pass

        await browser.close()

    return pd.DataFrame(cars)


async def main():
    df = await parse_drom_ru()
    df.to_csv('data/drom_cars.csv', index=False)
    print(f"Сохранено {len(df)} записей с Drom.ru")


if __name__ == "__main__":
    asyncio.run(main())