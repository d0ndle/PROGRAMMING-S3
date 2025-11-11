import sys
import math

def get_coefficient(name, arg_index=None):

    while True:
        value = None
        if arg_index is not None and len(sys.argv) > arg_index:
            try:
                value = float(sys.argv[arg_index])
            except ValueError:
                print(f"Ошибка: коэффициент {name} задан некорректно ({sys.argv[arg_index]}). Введите заново.")
                arg_index = None
        if value is None:
            try:
                value = float(input(f"Введите коэффициент {name}: "))
            except ValueError:
                print("Ошибка: введите число.")
                continue
        return value

def solve_biquadratic(a, b, c):
    if a == 0:
        print("Это не биквадратное уравнение (A = 0).")
        return []


    D = b ** 2 - 4 * a * c
    print(f"Дискриминант: D = {D}")

    roots = []

    if D < 0:
        print("Действительных корней нет.")
        return roots


    y1 = (-b + math.sqrt(D)) / (2 * a)
    y2 = (-b - math.sqrt(D)) / (2 * a)
    print(f"Корни квадратного уравнения по y: y1 = {y1}, y2 = {y2}")


    for y in [y1, y2]:
        if y >= 0:
            x1 = math.sqrt(y)
            x2 = -math.sqrt(y)
            roots.extend([x1, x2])

    if roots:
        print("Действительные корни уравнения:")
        for i, r in enumerate(sorted(roots)):
            print(f"x{i+1} = {r}")
    else:
        print("Действительных корней нет.")

    return roots

if __name__ == "__main__":
    a = get_coefficient("A", 1)
    b = get_coefficient("B", 2)
    c = get_coefficient("C", 3)

    solve_biquadratic(a, b, c)
