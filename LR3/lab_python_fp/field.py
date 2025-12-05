#Задача №1

def field(items, *args):
    assert len(args) > 0  # Проверяем, что передан хотя бы один ключ

    for item in items:  # Проходим по каждому словарю в списке
        if len(args) == 1:  # --- СЛУЧАЙ №1: передан один ключ ---
            key = args[0]  # единственный ключ
            value = item.get(key)  # забираем значение из словаря
            if value is not None:  # если значение НЕ None — выдаём
                yield value
        else:  # --- СЛУЧАЙ №2: передано несколько ключей ---
            result = {}  # временный словарь под выбранные поля
            for key in args:  # перебираем нужные ключи
                value = item.get(key)  # получаем значение
                if value is not None:  # пропускаем None
                    result[key] = value  # сохраняем только непустые

            # если получившийся словарь НЕ пустой → выдаём
            if result:
                yield result



#Запуск *******************************
goods = [
    {'title': 'Ковер', 'price': 2000, 'color': 'green'},
    {'title': 'Диван', 'color': 'black'}
]

# print(list(field(goods, 'title')))
# # ['Ковер', 'Диван']
#
# print(list(field(goods, 'title', 'price')))
# # [{'title': 'Ковер', 'price': 2000}, {'title': 'Диван'}]

