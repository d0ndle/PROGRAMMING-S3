from gen_random import gen_randoms

class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()

    def __next__(self):
        while True:
            item = next(self.items)

            key = item.lower() if self.ignore_case and isinstance(item, str) else item

            if key not in self.seen:
                self.seen.add(key)
                return item

    def __iter__(self):
        return self



# print("----- Пример 1 -----")
# data1 = [1, 1, 2, 2, 3, 1]
# for x in Unique(data1):
#     print(x)
#
# print("----- Пример 2 -----")
# data2 = gen_randoms(10, 1, 3)
# for x in Unique(data2):
#     print(x)
#
# print("----- Пример 3 -----")
# data3 = ['a', 'A', 'b', 'B', 'a']
# for x in Unique(data3):
#     print(x)
#
# print("----- Пример 4 (ignore_case=True) -----")
# data4 = ['a', 'A', 'b', 'B', 'a']
# for x in Unique(data4, ignore_case=True):
#     print(x)