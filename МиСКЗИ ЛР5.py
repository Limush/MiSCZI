import random
import sympy
import math


def Encrypt(text, e, n, encrypt, encrypt_text):
    for i in range(len(text)):
        encrypt_num = pow(text[i], e, n)
        encrypt.append(encrypt_num)
        encrypt_text.append(str(encrypt_num))
    return encrypt, encrypt_text


def Decrypt(encrypt, d, n, decrypt, decrypt_text):
    for i in range(len(encrypt)):
        decrypt_num = pow(encrypt[i], d, n)
        decrypt.append(decrypt_num)
        decrypt_text.append(str(decrypt_num))
    return decrypt, decrypt_text


alfavit = ' АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz'
p = sympy.randprime(2 ** 1022, 2 ** 1023)
q = sympy.randprime(2 ** 1022, 2 ** 1023)
while p == q:
    q = sympy.randprime(2 ** 1022, 2 ** 1023)
n = p * q
m = (p - 1) * (q - 1)
e = random.randint(2, m)
while math.gcd(e, m) != 1:
    e = random.randint(2, m)
d = pow(e, -1, m)
print(f"p = {p}\nq = {q}\nn = {n}\ne = {e}\nd = {d}\n"
      f"Длина p = {len(bin(p))} бит, Длина q = {len(bin(q))} бит, Длина n = {len(bin(n))} бит, Длина e = {len(bin(e))} бит, Длина d = {len(bin(d))} бит\n"
      f"\tОткрытый ключ:\n{e} {n}\n"
      f"\tЗакрытый ключ:\n{d} {n}\n")

while True:
    task = input('1 - Шифрование\n2 - Расшифрование\n--->')
    if task == '1':
        open_key = list(map(int, input('Введите Открытый ключ ->').split()))
        Text = input("Введите текст для шифрования -> ")
        text = [alfavit.find(i) for i in Text]

        encrypt, encrypt_text = Encrypt(text, open_key[0], open_key[1], [], [])
        print(f"\tЗашифруем фразу:\n{Text}\n"
              f"\tФраза в цифрах:\n{' '.join([str(i) for i in text])}\n"
              f"\tЗашифрованная последовательность:\n{' '.join(encrypt_text)}\n")
    elif task == '2':
        close_key = list(map(int, input('Введите Закрытый ключ ->').split()))
        encrypt = list(map(int, input("Введите зашифрованную последовательность ->").split()))
        decrypt, decrypt_text = Decrypt(encrypt, close_key[0], close_key[1], [], [])
        print(f"\tРасшифрованная последовательность в цифрах:\n{' '.join(decrypt_text)}\n"
              f"\tРасшифрованная последовательность:\n{''.join([alfavit[decrypt[i]] for i in range(len(decrypt))])}\n")
    else:
        break