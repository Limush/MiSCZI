import random
from prettytable import PrettyTable
import sympy
from math import sqrt

def inference(array_r, array_x, array_b, array_y, array_x_last, array_cheak):
    table = PrettyTable()
    table.field_names = [""] + [f"Аккредитация №{num+1}" for num in range(len(array_r))]
    table.add_row(["Сторона A: Выбирает число r, r<n"] + array_r)
    table.add_row(["Сторона A: Вычисляет число x = r^2 (mod n)"] + array_x)
    table.add_row(["Сторона В: Отправляет случайный бит b"] + array_b)
    table.add_row(["Сторона А: y = r          , если b=0\n"
                   "           y = r*S (mod n), если b=1"] + array_y)
    table.add_row(["Сторона B: x = r^2(mod n)       , если b=0\n"
                   "           x = (y**2 * V)(mod n), если b=1"] + array_x_last)
    table.add_row(["Выполнение аккредитации"] + array_cheak)
    for i in table.field_names:
        if i == '':
            table.align[f"{i}"] = "l"
        else:
            table.align[f"{i}"] = "c"
    return table


def Nod(a, b):
    if a == 0 or b == 0:
        return 0
    while True:
        a, b = b, a % b
        if b == 0:
            return a


def Generate(start, finish):
    prime1 = sympy.randprime(2**start, 2**finish)
    prime2 = sympy.randprime(2**start, 2**finish)
    return prime1 * prime2


def find(n):
    S = random.randint(1, int(sqrt(n)))
    while Nod(S, n) != 1:
        S = random.randint(1, int(sqrt(n)))
    V_reverse = pow(S, 2, n)
    return (S, V_reverse) if Nod(V_reverse, n) == 1 else (-1, -1)


n = Generate(1, random.randint(256, 512))
while True:
    S, V_reverse = find(n)
    if S != -1:
        break
V = pow(V_reverse, -1, n)
print(f"\t\t\tПодготовка к идентификации:\n"
      f"\t\tСторона А:\n"
      f"n    = {n}\n"
      f"Число длиной = {len(bin(n)[2:])} бит\n"
      f"V    = {V}\n"
      f"V^-1 = {V_reverse}\n"
      f"S    = {S}\n")
print(f"Открытый ключ ({V})\n"
      f"Закрытый ключ ({S})")

array_r, array_x, array_b, array_y, array_x_last, array_cheak = [], [], [], [], [], []
#   Начало цикла протокола
for i in range(20):
    error = 1 if random.randint(0, 100) < 15 else 0
    #   Сторона А:
    r = random.randint(1, n)
    x = r ** 2 % n

    #   Сторона В:
    b = random.randint(0, 1)

    #   Сторона А:
    if (b + error) % 2 == 0:
        y = r
    else:
        y = (r * S) % n

    #   Сторона В:
    if b == 0:
        x_B = y ** 2 % n
    else:
        x_B = (y ** 2 * V) % n

    array_r.append(r)
    array_x.append(x)
    array_b.append(b)
    array_y.append(y)
    array_x_last.append(x_B if error == 1 else x)
    array_cheak.append('Нет' if error == 1 else 'Да')
else:
    print(inference(array_r, array_x, array_b, array_y, array_x_last, array_cheak))
    print(f"Аккредитация прошла успешно в {array_cheak.count('Да')} случаях, что равняется {round(array_cheak.count('Да')/(i+1), 2) * 100}%")
    print(f"Проверка " + ("пройдена" if array_cheak.count('Да') >= 16 else "не пройдена"))


