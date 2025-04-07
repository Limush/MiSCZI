import random
import sympy
import math


alfavit = ' АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz'

p = sympy.randprime(2 ** 1021, 2 ** 1022)
q = random.randint(2, p)
while math.gcd(q, p) != 1:
    q = random.randint(2, p)
x = random.randint(2, p - 2)
y = pow(q, x, p)
print(f"p = {p}\nq = {q}\nx = {x}\ny = {y}\n"
      f"Открытый ключ:\n\t{p} {q} {y}\n"
      f"Закрытый ключ:\n\t{x}\n\n")

while True:
    task = input('1 - Шифрование\n2 - Расшифрование\n--->')
    if task == '1':
        def Encoding(M, p):
            k = random.randint(2, p - 2)
            return pow(q, k, p), pow((pow(y, k, p) * M), 1, p)

        open_key = list(map(int, input('Введите Открытый ключ ->').split()))
        p, q, y = open_key[0], open_key[1], open_key[2]
        text = input("Введите текст для шифрования ->")
        mass = [alfavit.find(i) for i in text]
        print(f"\t\tШифрование:\nСообщение:\n\t{text} = {' '.join([str(i) for i in mass])}")

        mass_encod = []
        for i in range(len(mass)):
            a, b = Encoding(mass[i], p)
            mass_encod.append(a)
            mass_encod.append(b)
        print(f"\n\tПолучился шифртекст:\n{' '.join([str(i) for i in mass_encod])}\n")
    elif task == '2':
        def Decoding(a, b, x, p):
            return pow((b * pow(a, (p - 1 - x), p)), 1, p)

        x = int(input("Введите Закрытый ключ ->"))
        p = int(input("p -> "))
        mass_encod = list(map(int, input("Введите зашифрованную последовательность ->").split(' ')))

        mass_decod = [Decoding(mass_encod[i * 2], mass_encod[i * 2 + 1], x, p) for i in range(len(mass_encod) // 2)]
        print(f"\n\t\tРасшифрование:\nТекст после расшифровки:\n{' '.join([str(i) for i in mass_decod])} = {''.join([alfavit[i] for i in mass_decod])}\n")
    else:
        break

