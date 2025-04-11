import random, sympy


def Nod(a, b):
    if a == 0 or b == 0:
        return 0
    while True:
        a, b = b, a % b
        if b == 0:
            return a


def generat_n():
    p, q = sympy.randprime(2 ** 1022, 2 ** 1023), sympy.randprime(2 ** 1022, 2 ** 1023)
    return p, q, p * q


alfavit = ' АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz'
p, q, n = generat_n()
while len(bin(n)) != 2048 or p == q:
    p, q, n = generat_n()
fi = (p - 1) * (q - 1)
e_open_key = random.randint(2, fi)
while Nod(e_open_key, fi) != 1:
    e_open_key = random.randint(2, fi)
d_close_key = pow(e_open_key, -1, fi)
print(f"p ({len(bin(p))} бит) = {p}\nq ({len(bin(q))} бит)  = {q}\nn ({len(bin(n))} бит)  = {n}\ne ({len(bin(e_open_key))} бит)  = {e_open_key}\nd ({len(bin(d_close_key))} бит)  = {d_close_key}")
print(f"\tОткрытый ключ:\n{e_open_key} {n}\n\tЗакрытый ключ:\n{d_close_key} {n}\n")

while True:
    task = input('1 - Шифрование\n2 - Расшифрование\n--->')
    if task == '1':
        open_key, Text = list(map(int, input('Введите Открытый ключ ->').split())), input("Введите текст для шифрования -> ")
        text = [alfavit.find(i) for i in Text]
        encrypt = [pow(text[i], open_key[0], open_key[1]) for i in range(len(text))]
        print(f"\tЗашифруем фразу:\n{Text}\n"
              f"\tФраза в цифрах:\n{' '.join([str(i) for i in text])}\n"
              f"\tЗашифрованная последовательность:\n{' '.join([str(i) for i in encrypt])}\n")
    elif task == '2':
        close_key, encrypt = list(map(int, input('Введите Закрытый ключ ->').split())), list(map(int, input("Введите зашифрованную последовательность ->").split()))
        decrypt = [pow(encrypt[i], close_key[0], close_key[1]) for i in range(len(encrypt))]
        print(f"\tРасшифрованная последовательность в цифрах:\n{' '.join([str(i) for i in decrypt])}\n"
              f"\tРасшифрованная последовательность:\n{''.join([alfavit[decrypt[i]] for i in range(len(decrypt))])}\n")
    else:
        break