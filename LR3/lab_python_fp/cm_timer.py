import time
from time import sleep
from contextlib import contextmanager

#Вариант 1:
class cm_timer_1:
    def __enter__(self):
        self.start = time.time()      # фиксируем время входа
        return self                   # возвращать можно что угодно (или ничего)

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()             # фиксируем время выхода
        print("time:", end - self.start)

#Вариант 2:
@contextmanager
def cm_timer_2():
    start = time.time()               # фиксируем время входа
    try:
        yield                         # запускаем тело with-блока
    finally:
        end = time.time()             # время выхода (даже при ошибке в блоке)
        print("time:", end - start)

# with cm_timer_1():
#     sleep(2.5)
#
# with cm_timer_2():
#     sleep(1.3)