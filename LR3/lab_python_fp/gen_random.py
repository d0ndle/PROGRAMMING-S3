import random

def gen_randoms(num_count, begin, end):
    for _ in range(num_count):                # повторяем нужное количество раз
        yield random.randint(begin, end)      # выдаём число и "замораживаемся"


# for x in gen_randoms(5, 1, 3):
#     print(x)
