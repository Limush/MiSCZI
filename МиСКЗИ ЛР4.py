import random
from prettytable import PrettyTable
import sympy
from math import sqrt


def inference(array_r, array_x, array_b, array_y, array_x_last, array_cheak):
    table = PrettyTable()
    table.add_row(["Сторона A: Выбирает число r, r<n"] + array_r)
    table.add_row(["Сторона A: Вычисляет число x = r^2 (mod n)"] + array_x)
    table.add_row(["Сторона В: Отправляет случайную двоичную строку b"] + array_b)
    table.add_row(["Сторона А: y = (r*(S1^b1*S2^b2*...*Sk^bk))(mod n)"] + array_y)
    table.add_row(["Сторона B: x = (y^2*(V1^b1*V2^b2*...*Vk^bk))(mod n)"] + array_x_last)
    table.add_row(["Выполнение аккредитации"] + array_cheak)

    table.field_names = [""] + [f"Аккредитация №{num+1}" for num in range(len(array_r))]
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
K = 5
prohibition = 0
all = 0
for series in range(4):
    Open_key = []
    Secret_key = []
    for i in range(K):
        while True:
            S, V_reverse = find(n)
            if S != -1:
                break
        V = pow(V_reverse, -1, n)
        Open_key.append(V)
        Secret_key.append(S)
    print(f"Открытый ключ = {Open_key}\n"
          f"Закрытый ключ = {Secret_key}")

    array_r, array_x, array_b, array_y, array_x_last, array_cheak = [], [], [], [], [], []
    for count in range(5):
        #       Сторона А:
        r = random.randint(0, n)
        x = r ** 2 % n

        #       Сторона В:
        b = []
        while True:
            for i in range(K):
                b.append(random.randint(0, 1))
            if len(b) == K and 1 in b:
                break
            elif len(b) == K and 1 not in b:
                b = []
        b_A = b.copy()
        error = 1 if random.randint(0, 100) < 10 else 0
        b_A[0] = (b_A[0] + error) % 2

        #       Сторона А:
        y = r
        for i in range(K):
            y *= Secret_key[i] ** b_A[i]
        y = y % n

        #       Сторона В:
        x_B = y**2
        for i in range(K):
            x_B *= Open_key[i] ** b[i]
        x_B = x_B % n

        array_r.append(r)
        array_x.append(x)
        array_b.append(b)
        array_y.append(y)
        array_x_last.append(x_B)
        array_cheak.append('Нет' if x != x_B else 'Да')
    prohibition += 1 if array_cheak.count('Нет') >= 2 else 0
    all += array_cheak.count('Да')
    print(f"{'\t'*15}Цикл {series + 1}:")
    print(inference(array_r, array_x, array_b, array_y, array_x_last, array_cheak))
    print(f"Аккредитация прошла успешно в {array_cheak.count('Да')} случаях")
    print()
print(f"По результату 20 проверок Аккредитация прошла успешно в {all} случаях, что равняется {round(all / 20, 2) * 100}%\n"
      f"Проверка " + ("пройдена" if (prohibition == 0 or all >= 18) else "не пройдена"))
