import json
import sys
import random

from field import field
from unique import Unique
from print_result import print_result
from cm_timer import cm_timer_1

path = sys.argv[1]  # путь к файлу передаётся при запуске скрипта

with open(path, encoding='utf-8') as f:
    data = json.load(f)


# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(arg):
    # отсортированный список профессий без повторов, сортировка и уникальность без учёта регистра
    return sorted(Unique(field(arg, 'job-name'), ignore_case=True), key=str.lower)


@print_result
def f2(arg):
    # оставить только те строки, которые начинаются со слова "программист" (без учёта регистра)
    return list(filter(lambda x: x.lower().startswith('программист'), arg))


@print_result
def f3(arg):
    # добавить " с опытом Python" к каждой строке
    return list(map(lambda x: x + ' с опытом Python', arg))


@print_result
def f4(arg):
    # сгенерировать зарплаты и склеить со строками
    salaries = [random.randint(100000, 200000) for _ in arg]
    return list(map(lambda pair: f'{pair[0]}, зарплата {pair[1]} руб.', zip(arg, salaries)))


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))