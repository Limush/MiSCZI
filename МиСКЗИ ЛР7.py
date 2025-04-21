import binascii
import hashlib
import random
import sympy
from tkinter import filedialog

def calculate_file_hash(filename, algorithm='sha256', buffer_size=65536):
    hash_obj = hashlib.new(algorithm)

    with open(filename, 'rb') as f:
        while chunk := f.read(buffer_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def Nod(a, b):
    if a == 0 or b == 0:
        return 0
    while True:
        a, b = b, a % b
        if b == 0:
            return a


def string_to_hex(input_string):
    bytes_data = input_string.encode('utf-8')
    hex_data = bytes_data.hex()
    return hex_data


def generat_n():
    start = 1022
    p, q = sympy.randprime(2 ** start, 2 ** (start + 1)), sympy.randprime(2 ** start, 2 ** (start + 1))
    return p, q, p * q


def generate_key():
    p, q, n = generat_n()
    while p == q or len(bin(n)) != 2048:
        p, q, n = generat_n()
    fi = (p - 1) * (q - 1)
    e_open_key = random.randint(2, fi)
    while Nod(e_open_key, fi) != 1:
        e_open_key = random.randint(2, fi)
    d_close_key = pow(e_open_key, -1, fi)
    return e_open_key, d_close_key, n




file_path = filedialog.askopenfilename(title="Open Filename",
                                       filetypes=(("Word Files", "*.docx"),
                                                  ("TXT Files", "*.txt"),
                                                  ("All Files", "*.*")))
task = input('1 - Подписать\n2 - Проверить\n--->')
if task == '1':
    e, d, n = generate_key()
    print(f"e = {e}\n"
          f"d = {d}\n"
          f"n = {n}\n")
    n = int(input("Введите n ->"))
    e = int(input("Введите открытый ключ ->"))
    hash_file_hex = int(string_to_hex(calculate_file_hash(file_path, 'sha256')))
    S = pow(hash_file_hex, e, n)
    print(f"hash        = {hash_file_hex}\n"
          f"Подписанный = {S}\n")
    with open("RSA.txt", 'a', encoding="utf-8") as file:
        file.seek(0)
        file.truncate()
        file.write(f"e           = {e}\n"
                   f"d           = {d}\n"
                   f"n           = {n}\n"
                   f"hash        = {hash_file_hex}\n"
                   f"Подписанный = {S}\n")
else:
    n = int(input("Введите n ->"))
    d = int(input("Введите закрытый ключ ->"))
    S = int(input("Введите Подпись ->"))
    hash_file_hex = int(string_to_hex(calculate_file_hash(file_path, 'sha256')))
    H = pow(S, d, n)
    print(f"hash        = {hash_file_hex}\n"
          f"Подписанный = {S}\n"
          f"Проверка    = {H}")
    if H == hash_file_hex:
        print(f"Файл не изменялся\n")
    else:
        print(f"Файл изменен\n")