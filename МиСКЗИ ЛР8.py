import hashlib
import random
import sympy
from tkinter import filedialog


def calculate_file_hash(filename, algorithm='gost34112012', buffer_size=65536):
    hash_obj = hashlib.new(algorithm)
    with open(filename, 'rb') as f:
        while chunk := f.read(buffer_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def string_to_hex(input_string):
    bytes_data = input_string.encode('utf-8')
    hex_data = bytes_data.hex()
    return hex_data


def generate_p_q():
    q = sympy.randprime(2 ** 254 + 1, 2 ** 256 - 1)
    start, finish = 2 ** 509 + 1, 2 ** 512 - 1
    while True:
        k_min = (start - 1) // q
        k_max = (finish - 1) // q
        k = random.randint(k_min, k_max)
        p = k * q + 1
        if start < p < finish and sympy.isprime(p):
            return p, q


def generate_key():
    while True:
        p, q = generate_p_q()
        d = random.randint(2, p - 2)
        f = pow(d, (p-1)//q, p)
        if f != 1:
            a = f
            break
    x = random.randint(2, q - 1)
    y = pow(a, x, p)
    print(f"p = {p}\n"
          f"q = {q}\n"
          f"a = {a}\n"
          f"x = {x}\n"
          f"y = {y}\n")
    return (p, q, a, y), x


def Subscribe(p, q, a, x, HASH):
    while True:
        HASH = 1 if HASH % q == 0 else HASH
        while True:
            k = random.randint(1, q - 1)
            r = pow(a, k, p) % q
            if r != 0:
                break
        s = (x * r + k * HASH) % q
        if s != 0:
            break
    return r, s


def Verify_the_signature(p, q, a, y, HASH, r, s):
    v = pow(HASH, q - 2, q)
    z1 = (s * v) % q
    z2 = ((q - r) * v) % q
    u = (pow(a, z1, p) * pow(y, z2, p) % p) % q
    if u == r:
        return True
    else:
        return False


open_key, close_key = generate_key()
print(f"Открытый ключ:\n"
      f"\t{' '.join([str(i) for i in open_key])}\n"
      f"Закрытый ключ:\n"
      f"\t{close_key}")

file_path = filedialog.askopenfilename(title="Open Filename",
                                       filetypes=(("TXT Files", "*.txt"),
                                                  ("Word Files", "*.docx"),
                                                  ("All Files", "*.*")))
task = input('1 - Подписать\n2 - Проверить\n--->')
if task == '1':
    p = int(input("Введите p ->"))
    q = int(input("Введите q ->"))
    a = int(input("Введите a ->"))
    y = int(input("Введите y ->"))
    x = int(input("Введите x ->"))
    hash_file_hex = int(string_to_hex(calculate_file_hash(file_path, 'sha256')))
    subscribe = Subscribe(p, q, a, x, hash_file_hex)
    print(f"hash        = {hash_file_hex}\n"
          f"Подписанный = {subscribe[0]} {subscribe[1]}\n")
    with open("GOST.txt", 'a', encoding="utf-8") as file:
        file.seek(0)
        file.truncate()
        file.write(f"p           = {p}\n"
                   f"q           = {q}\n"
                   f"a           = {a}\n"
                   f"y           = {y}\n"
                   f"x           = {x}\n"
                   f"hash        = {hash_file_hex}\n"
                   f"Подписанный = {subscribe[0]} {subscribe[1]}\n")
else:
    p = int(input("Введите p ->"))
    q = int(input("Введите q ->"))
    a = int(input("Введите a ->"))
    y = int(input("Введите y ->"))
    r = int(input("Введите r ->"))
    s = int(input("Введите s ->"))
    hash_file_hex = int(string_to_hex(calculate_file_hash(file_path, 'sha256')))
    verify = Verify_the_signature(p, q, a, y, hash_file_hex, r, s)
    with open("GOST.txt", 'a', encoding="utf-8") as file:
        file.write(f"\n\n\tПроверка подписи:\n"
                   f"p           = {p}\n"
                   f"q           = {q}\n"
                   f"a           = {a}\n"
                   f"y           = {y}\n"
                   f"Подпись     = {r} {s}\n"
                   f"hash        = {hash_file_hex}\n"
                   f"Изменения   = {"Нет" if verify else "Да"}\n")
    if verify:
        print(f"Файл не изменялся\n")
    else:
        print(f"Файл изменен\n")