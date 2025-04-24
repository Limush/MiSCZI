import random
import sympy
from Functions.Simplicity_check import Simplicity_check


def Nod(a, b):
    if a == 0 or b == 0:
        return 0
    while True:
        a, b = b, a % b
        if b == 0:
            return a


alfavit = ' АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz'
# p = sympy.randprime(2 ** 1021, 2 ** 1022)
# while len(bin(p)) != 1024 or Simplicity_check(p) == "Составное":
#     p = sympy.randprime(2 ** 1021, 2 ** 1022)
p = sympy.randprime(2 ** 2045, 2 ** 2046)
while len(bin(p)) != 2048 or Simplicity_check(p) == "Составное":
    p = sympy.randprime(2 ** 1021, 2 ** 1022)
q = random.randint(2, p)
while Nod(q, p) != 1:
    q = random.randint(2, p)
x = random.randint(2, p - 1)
y = pow(q, x, p)
print(f"p ({len(bin(p))} бит) = {p}\nq ({len(bin(q))} бит) = {q}\nx ({len(bin(x))} бит) = {x}\ny ({len(bin(y))} бит) = {y}\nОткрытый ключ:\n\t{p} {q} {y}\nЗакрытый ключ:\n\t{x}\n")
while True:
    task = input('Выберите:\n\tШифрование\n\tРасшифрование\n--->')
    if task == 'Шифрование':
        open_key, text = list(map(int, input('Введите Открытый ключ ->').split())), input("Введите текст для шифрования ->")
        p, q, y = open_key[0], open_key[1], open_key[2]
        open_text = [alfavit.find(i) for i in text]
        encrypt = []
        for i in range(len(open_text)):
            k, M = random.randint(2, p - 1), open_text[i]
            a, b = pow(q, k, p), (pow(y, k, p) * M) % p
            encrypt.extend([a, b])
        print(f"\t\tШифрование:\n\tСообщение:\n{text} = {'; '.join([str(i) for i in open_text])}\n\tПолучился шифртекст:\n{' '.join([str(i) for i in encrypt])}\n\n")
    elif task == 'Расшифрование':
        x, p, encrypt = int(input("Введите Закрытый ключ ->")), int(input("p -> ")), list(map(int, input("Введите зашифрованную последовательность ->").split(' ')))
        decrypt = []
        for i in range(len(encrypt) // 2):
            a, b = encrypt[i * 2], encrypt[i * 2 + 1]
            decrypt.append((b * pow(a, (p - 1 - x), p)) % p)
        print(f"\n\t\tРасшифрование:\n\tТекст после расшифровки:\n{' '.join([str(i) for i in decrypt])} = {''.join([alfavit[i] for i in decrypt])}\n\n")
    else: break