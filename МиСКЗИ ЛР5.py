import random
import sympy


def Nod(a, b):
    if a == 0 or b == 0:
        return 0
    while True:
        a, b = b, a % b
        if b == 0:
            return a


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
while True:
    task = input('1 - Шифрование\n2 - Расшифрование\n--->')
    if task == '1':
        p = sympy.randprime(2 ** 1022, 2 ** 1023)
        q = sympy.randprime(2 ** 1022, 2 ** 1023)
        n = p * q
        m = (p - 1) * (q - 1)
        e = random.randint(2, m)
        while Nod(e, m) != 1:
            e = random.randint(2, m)
        d = pow(e, -1, m)
        print(len(bin(e)))
        print(f"\nДлина p = {len(bin(p))} бит, Длина q = {len(bin(q))} бит, Длина n = {len(bin(n))} бит, Длина e = {len(bin(e))} бит, Длина d = {len(bin(d))} бит\n"
              f"\tОткрытый ключ:\n{e} {n}\n"
              f"\tЗакрытый ключ:\n{d} {n}\n")

        Text = input("Введите текст для шифрования -> ")
        text = [alfavit.find(i) for i in Text]

        encrypt, encrypt_text = Encrypt(text, e, n, [], [])
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