#https://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://quotes.toscrape.com"


def scrape_quotes(max_pages=5):
    """
    Функция ходит по страницам сайта и собирает цитаты в список словарей.

    """
    all_rows = []

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/page/{page}/"
        print("Скачиваю страницу:", url)

        response = requests.get(url)
        if response.status_code != 200:
            print("Страница не найдена, останавливаемся.")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # находим все блоки с цитатами
        quote_blocks = soup.find_all("div", class_="quote")
        if not quote_blocks:
            print("Цитаты не найдены, вероятно, страниц больше нет.")
            break

        for block in quote_blocks:
            # текст цитаты
            text_tag = block.find("span", class_="text")
            text = text_tag.get_text(strip=True) if text_tag else ""

            # автор
            author_tag = block.find("small", class_="author")
            author = author_tag.get_text(strip=True) if author_tag else ""

            # теги (их несколько)
            tag_elements = block.find_all("a", class_="tag")
            tags_list = [t.get_text(strip=True) for t in tag_elements]

            # формируем одну строку датасета (одна цитата)
            row = {
                "text": text,                      # текст цитаты
                "author": author,                  # автор
                "tags": ", ".join(tags_list),      # теги через запятую в одной ячейке
                "num_tags": len(tags_list),        # сколько тегов у цитаты
                "text_len": len(text),             # длина текста цитаты
            }
            all_rows.append(row)

    return all_rows


def main():
    # 1. СКАЧИВАЕМ ДАННЫЕ И ДЕЛАЕМ ДАТАСЕТ
    data = scrape_quotes(max_pages=5)  # соберём первые 5 страниц
    print(f"\nСобрано цитат: {len(data)}")

    # превращаем список словарей в табличный DataFrame
    df = pd.DataFrame(data)

    print("\nПервые 5 строк датасета:")
    print(df.head())

    # 2. СОХРАНЯЕМ В CSV
    csv_filename = "quotes_dataset.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"\nДатасет сохранён в файл: {csv_filename}")

    # 3. РАЗВЕДОЧНЫЙ АНАЛИЗ ДАННЫХ (EDA)

    print("\n=== ОБЩАЯ ИНФОРМАЦИЯ О ДАТАСЕТЕ ===")
    print(df.info())

    print("\n=== ОПИСАТЕЛЬНАЯ СТАТИСТИКА ПО ЧИСЛОВЫМ ПОЛЯМ ===")
    print(df.describe())  # num_tags, text_len

    print("\n=== ТОП-5 АВТОРОВ ПО КОЛИЧЕСТВУ ЦИТАТ ===")
    print(df["author"].value_counts().head(5))

    print("\n=== ТОП-10 ТЕГОВ ===")
    # столбец tags хранит строки типа "life, love, humor"
    tags_series = df["tags"].str.split(", ")
    all_tags = tags_series.explode()          # превращаем списки тегов в одну колонку
    all_tags = all_tags.dropna()              # убираем пустые значения, если есть
    print(all_tags.value_counts().head(10))

    print("\n=== СРЕДНЯЯ ДЛИНА ЦИТАТЫ ===")
    print(df["text_len"].mean())

    print("\n=== ПРИМЕР ПАРЫ САМЫХ ДЛИННЫХ ЦИТАТ ===")
    longest = df.sort_values(by="text_len", ascending=False).head(3)
    print(longest[["author", "text_len", "text"]])


if __name__ == "__main__":
    main()
