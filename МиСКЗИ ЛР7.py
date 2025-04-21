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


e, d, n = generate_key()
print(f"e = {e}\n"
      f"d = {d}\n"
      f"n = {n}\n")

file_path = filedialog.askopenfilename(title="Open Filename",
                                       filetypes=(("Word Files", "*.docx"),
                                                  ("TXT Files", "*.txt"),
                                                  ("All Files", "*.*")))
task = input('1 - Подписать\n2 - Проверить\n--->')
print(1+1)
if task == '1':
    # file_path = select()
    n = int(input("Введите n ->"))
    e = int(input("Введите открытый ключ ->"))
    hash_file_hex = int(string_to_hex(calculate_file_hash(file_path, 'sha256')))
    S = pow(hash_file_hex, int(e), int(n))
    print(f"hash        = {hex(hash_file_hex)}\n"
          f"Подписанный = {hex(S)}\n")
    with open("RSA.txt", 'a', encoding="utf-8") as file:
        file.seek(0)
        file.truncate()
        file.write(f"e           = {e}\n"
                   f"d           = {d}\n"
                   f"n           = {n}\n"
                   f"hash        = {hex(hash_file_hex)}\n"
                   f"Подписанный = {hex(S)}\n")
else:
    n = int(input("Введите n ->"))
    d = int(input("Введите закрытый ключ ->"))
    S = int(input("Введите Подпись ->"), 16)
    hash_file_hex = int(string_to_hex(calculate_file_hash(file_path, 'sha256')))
    H = pow(S, int(d), int(n))
    print(f"hash        = {hex(hash_file_hex)}\n"
          f"Подписанный = {hex(S)}\n"
          f"Проверка    = {hex(H)}")
    if H == hash_file_hex:
        print(f"Файл не изменялся\n")
    else:
        print(f"Файл изменен\n")

# e = 1253987889059162499970128862445478624173386500694934056394466207527457162604860918486992457691761009960034726783169033494956345863011403847343122694920728298982732422589174149975600738819717398027172442041775745727634963174670421994436697049274850617265515116845709394523602114492697093066962595599251062444864638402214562165749139747484189756289392989880938028266321006864063063969455754608068431898923133330782470402152063290953415302535532154655608321682312842987370393422605223833933628452355605793946976048462079670661121677499894085834883849311926853705092465007571709864343379907280905713112339351680756277043
# d = 1677863587361528836209700896973726883945290266562667117216968423021032432305536286089748810370654994544060169735544942983482904519500028955850320249242011964760854377555464687426279575295014930144860038423093949924471481816812745670901361034539416485913841447434387873910033738764900690013817600733752171490336907708969626718898373895620101146286165374623456950616234405863836870059612530171393994052401831918854156551895500154527502539403586575333037599641873487969145673779598159361000274446694207629658738212225974689967260609260881881731085669210779937452260628471153472931447166051081139762606867941581231269491
# n = 4486196572282187433306991289037750814192419540868918659018968286979622603799606841513851291248742722038762684221991458053924279124882383526742066567853433141944123542756546128411885410975146641986800444370683801792170347231043956788723713848955207918424314364212519626540569904648512501910110396040043477206911032323118975001016661342374485346993378593552723185844435552945370850662950228830597700891862799425860851664488196914001791253069637262557386675529194256934449295007004990798983819879094830719666941869810251013814952358600652214732481603488907362113785423029435488173726702156152890206306157391167499391687
