
import unittest

from refRK1 import get_data, task_a1, task_a2, task_a3


class TestVariant12A(unittest.TestCase):
    def setUp(self):
        self.tools, self.languages, self.lang_tools = get_data()

    def test_task_a1(self):
        # Проверяем связь 1 -> M и порядок
        result = task_a1(self.tools, self.languages)

        expected = [
            ("IntelliJ IDEA", ["Java"]),
            ("PyCharm", ["Python"]),
            ("Visual Studio Code", ["C#", "JavaScript"]),
            ("Xcode", ["Swift"]),
        ]

        self.assertEqual(result, expected)

    def test_task_a2(self):
        # Проверяем суммы вакансий по M <-> M и сортировку
        result = task_a2(self.tools, self.languages, self.lang_tools)

        expected = [
            ("Visual Studio Code", 4050),  # Python + Java + C# + JavaScript
            ("IntelliJ IDEA", 2400),       # Java + JavaScript
            ("PyCharm", 950),              # Python
            ("Xcode", 400),                # Swift
        ]

        self.assertEqual(result, expected)

    def test_task_a3(self):
        # Проверяем выборку по слову "code" в названии
        result = task_a3(self.tools, self.languages, self.lang_tools, keyword="code")

        expected = {
            "Visual Studio Code": ["C#", "Java", "JavaScript", "Python"],
            "Xcode": ["Swift"],
        }

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
