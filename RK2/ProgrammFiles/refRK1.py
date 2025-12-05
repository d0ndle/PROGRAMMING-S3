



def get_data():
    # Список средств разработки
    tools = [
        {"id": 1, "title": "Visual Studio Code"},
        {"id": 2, "title": "PyCharm"},
        {"id": 3, "title": "IntelliJ IDEA"},
        {"id": 4, "title": "Xcode"},
    ]

    # Список языков программирования
    languages = [
        {"id": 1, "name": "Python",      "vacancies": 950,  "primary_tool_id": 2},
        {"id": 2, "name": "Java",        "vacancies": 1100, "primary_tool_id": 3},
        {"id": 3, "name": "C#",          "vacancies": 700,  "primary_tool_id": 1},
        {"id": 4, "name": "Swift",       "vacancies": 400,  "primary_tool_id": 4},
        {"id": 5, "name": "JavaScript",  "vacancies": 1300, "primary_tool_id": 1},
    ]

    # Связь многие-ко-многим: язык ↔ средство разработки
    lang_tools = [
        # Python
        {"lang_id": 1, "tool_id": 1},
        {"lang_id": 1, "tool_id": 2},
        # Java
        {"lang_id": 2, "tool_id": 1},
        {"lang_id": 2, "tool_id": 3},
        # C#
        {"lang_id": 3, "tool_id": 1},
        # Swift
        {"lang_id": 4, "tool_id": 4},
        # JavaScript
        {"lang_id": 5, "tool_id": 1},
        {"lang_id": 5, "tool_id": 3},
    ]

    return tools, languages, lang_tools


# ====== ЗАПРОС А1 (1 -> M) ======

def task_a1(tools, languages):
    """
    А1: 1 -> M
    Для каждого средства разработки вернуть список языков,
    где это средство является ОСНОВНЫМ.
    Результат: список кортежей (название_средства, [список_языков])
    """
    result = []

    # сортируем инструменты по названию
    tools_sorted = sorted(tools, key=lambda t: t["title"].lower())

    for tool in tools_sorted:
        langs_for_tool = []

        # ищем языки, у которых primary_tool_id = id этого инструмента
        for lang in languages:
            if lang["primary_tool_id"] == tool["id"]:
                langs_for_tool.append(lang["name"])

        # сортируем языки по алфавиту
        langs_for_tool.sort()

        # в результат кладём кортеж (строка, список)
        result.append((tool["title"], langs_for_tool))

    return result


# ====== ЗАПРОС А2 (M <-> M, сумма вакансий) ======

def task_a2(tools, languages, lang_tools):
    """
    А2: M <-> M
    Для каждого средства разработки посчитать СУММУ вакансий
    по всем связанным с ним языкам (через lang_tools).
    Результат: список (название_средства, сумма_вакансий), отсортирован по убыванию.
    """
    result = []

    for tool in tools:
        # Сначала найдём id языков, связанных с этим инструментом
        lang_ids = []
        for lt in lang_tools:
            if lt["tool_id"] == tool["id"]:
                lang_ids.append(lt["lang_id"])

        # Теперь считаем сумму вакансий по этим языкам
        total = 0
        for lang in languages:
            if lang["id"] in lang_ids:
                total += lang["vacancies"]

        result.append((tool["title"], total))

    # сортируем по сумме вакансий по убыванию
    result.sort(key=lambda pair: pair[1], reverse=True)
    return result


# ====== ЗАПРОС А3 (M <-> M + фильтр по слову в названии) ======

def task_a3(tools, languages, lang_tools, keyword="code"):
    """
    А3: M <-> M + фильтр по названию средства разработки.
    Находим средства, в названии которых есть keyword (по умолчанию "code"),
    и возвращаем словарь: {название_средства: [список_языков]}.
    """
    keyword = keyword.lower()
    result = {}

    for tool in tools:
        # проверяем, есть ли keyword в названии
        if keyword in tool["title"].lower():
            # собираем id языков для этого инструмента
            lang_ids = []
            for lt in lang_tools:
                if lt["tool_id"] == tool["id"]:
                    lang_ids.append(lt["lang_id"])

            # собираем имена языков
            langs_for_tool = []
            for lang in languages:
                if lang["id"] in lang_ids:
                    langs_for_tool.append(lang["name"])

            # убираем дубли и сортируем
            langs_for_tool = sorted(set(langs_for_tool))

            result[tool["title"]] = langs_for_tool

    return result


# ====== ПРОСТО ВЫВОД ДЛЯ ПРОВЕРКИ (НЕ ДЛЯ ТЕСТОВ) ======

def main():
    tools, languages, lang_tools = get_data()

    print("А1:")
    for tool_title, langs in task_a1(tools, languages):
        print(tool_title, "->", ", ".join(langs) if langs else "-")

    print("\nА2:")
    for tool_title, total in task_a2(tools, languages, lang_tools):
        print(tool_title, "->", total)

    print("\nА3:")
    result = task_a3(tools, languages, lang_tools)
    for tool_title, langs in result.items():
        print(tool_title, "->", ", ".join(langs) if langs else "-")


if __name__ == "__main__":
    main()
