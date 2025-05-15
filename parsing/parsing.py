import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_imdb_top_tv():
    base_url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    all_series = []

    try:
        print("Получаем топ сериалов IMDb")

        # Парсим все страницы
        for start in range(0, 250, 25):  # 250 - примерное максимальное количество сериалов
            url = f"{base_url}&start={start}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            series = soup.select('li.ipc-metadata-list-summary-item')

            # Парсим данные с текущей страницы
            page_series = [
                {
                    'Название': item.select_one('h3.ipc-title__text').get_text(strip=True).split('. ')[1],
                    'Год': item.select_one('span.cli-title-metadata-item').get_text(strip=True),
                    'Рейтинг': item.select_one('span.ipc-rating-star').get_text(strip=True).split()[0],
                    'Позиция': i + 1 + start  # Учитываем смещение позиций
                }
                for i, item in enumerate(series)
            ]

            all_series.extend(page_series)

            # Проверяем, есть ли еще элементы
            if not series:
                break

        df = pd.DataFrame(all_series)
        df.to_excel('top_tv_series.xlsx', index=False)

        print("\nПервые 10 сериалов из топа:")
        print(df.head(10))

        return df

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


if __name__ == "__main__":
    parse_imdb_top_tv()
