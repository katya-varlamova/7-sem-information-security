import random
import sys
def eratos(n):
    bools = []
    for i in range(n):
        bools.append(True)
    for i in range(2, n):
        if bools[i] == True:
            for j in range(i + i, n, i):
                bools[j] = False
    
    primes = []    
    for i in range(2, n):
        if bools[i] == True:
            primes.append(i)
    return primes

def matr_mult(a, b):

    c = [[
        a[0][0] * b[0][0] + a[0][1] * b[1][0],
        a[0][0] * b[0][1] + a[0][1] * b[1][1]
        ],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0],
        a[1][0] * b[0][1] + a[1][1] * b[1][1]]]
    return c

def gcd(a, b):
    while b:
        tmp = a
        a = b
        b = tmp % b
    return a

def egcd(a, b):
    em = [[1, 0],
          [0, 1]]
    r = a % b
    while r:
        em = matr_mult(em, [[0, 1], [1, -(a // b)]])
        a = b
        b = r
        r = a % b

    return (em[0][1], em[1][1])

def fast_pow(a, k, n):
    r = 1
    while k != 0:
        if k % 2 != 0:
            r = (r * a) % n
            k -= 1
        else:
            a = (a * a) % n
            k //=  2
    return r

    
def generate_keys_rsa(p, q):
    if p == q: # cant be the same
        return
    n = p * q
    f = (p - 1) * (q - 1)

    m = eratos(f)
    ran = random.randint(len(m) // 2, len(m) - 1)

    e = m[ran]
    while gcd(e, f) != 1:
        e = m[ran]
    
    d = egcd(e, f)[0]
    if d < 0:
        d += f
    
    return (e, d, n)

def encrypt_rsa(msg, e, n):
    enc = []
    for byte in msg:
        enc.append(fast_pow(byte, e, n))
    return enc

def decrypt_rsa(msg, d, n):
    dec = []
    for byte in msg:
        dec.append(fast_pow(byte, d, n))
    return dec

def units():
    arr = []
    for i in range(80000, 80100):
        arr.append(i + 2)


    er = eratos(1000)
    for i in range(1000):
        ra = random.randint(len(er) // 4, len(er) - 1)
        rb = random.randint(len(er) // 4, len(er) - 1)
        while ra == rb:
            ra = random.randint(len(er) // 4, len(er) - 1)
            rb = random.randint(len(er) // 4, len(er) - 1)
        
        e, d, n = generate_keys_rsa(er[ra], er[rb])
        m = encrypt_rsa(arr, e, n)
        m = decrypt_rsa(m, d, n)
        if arr != m:
            print("error: ")
            print(arr)
            print(m)
            print(ra, rb)
            print()


def create_bin_file(fn, info):
    with open(fn, "wb") as file:
        file.write(info)

def read_bin_file(fn):
    with open(fn, "rb") as file:
        return file.read()
    
def bytes_to_int_arr(ba):
    i_arr = []
    for byte in ba:
        i_arr.append(byte)
    return i_arr

def int_arr_to_bytes(i_arr):
    ba = bytearray()
    for i in i_arr:
        ba.append(i)
    return ba
def int_to_bits(i, bts):
    res = []
    for j in range(bts * 8):
        res.append(0)
    j = bts * 8 - 1
    while i > 0:
        res[j] = i % 2
        i //= 2
        j -= 1
    return res


def bits_to_int(arr, byte):
    s = 0
    st = 1
    for i in range(len(arr)):
        s += arr[byte * 8 - 1 - i] * st
        st *= 2
    return s


def int_arr_to_bits(i_arr, bts):
    bits = []
    for i in range(len(i_arr) ):
        bits += int_to_bits(i_arr[i], bts)
    return bits


def byte_to_bytes_arr(arr, bts):
    res = []
    for i in range(len(arr) // bts):
        res.append(bits_to_int(int_arr_to_bits(arr[bts * i : bts * i + bts], 1), bts))
    return res

def bytes_to_byte_arr(arr, bts):
    res = []
    for i in range(len(arr)):
        bits = int_arr_to_bits([arr[i]], bts)
        for j in range(bts):
            res.append(bits_to_int(bits[j * 8 : j * 8 + 8], 1))
    return res

if len(sys.argv) < 2:
    exit(0)
    
if sys.argv[1] == '-u':
    units()
    
if sys.argv[1] == '-g':
    e, d, n = generate_keys_rsa(1051, 977) # 20 bits
    with open("key.pub", 'w') as f:
        print('{} {}'.format(e, n), file = f)
    with open("key.pri", 'w') as f:
        print('{} {}'.format(d, n), file = f)
        
if sys.argv[1] == '-e':
    ifn = sys.argv[2]
    ofn = sys.argv[3]
    e = 0
    n = 0
    with open("key.pub") as f:
        e, n = map(int, f.readline().split())
        
    i_arr = bytes_to_int_arr(read_bin_file(ifn))
    ex = 0
    if len(i_arr) % 2 != 0:
        i_arr.append(0)
        ex = 1
    with open("extra.txt", 'w') as extra:
        extra.write(str(ex))
            
    
    arr = byte_to_bytes_arr(i_arr, 2)

    enc = encrypt_rsa(arr, e, n)

    res = bytes_to_byte_arr(enc, 3)
    
    create_bin_file(ofn, int_arr_to_bytes(res))


if sys.argv[1] == '-d':
    ifn = sys.argv[2]
    ofn = sys.argv[3]
    e = 0
    n = 0
    with open("key.pri") as f:
        d, n = map(int, f.readline().split())
        
    i_arr = bytes_to_int_arr(read_bin_file(ifn))

    arr = byte_to_bytes_arr(i_arr, 3)

    dec = decrypt_rsa(arr, d, n)

    res = bytes_to_byte_arr(dec, 2)

    with open("extra.txt", 'r') as extra:
        ex = int(extra.readline())
        if ex == 1:
            res = res[:len(res) - 1]
    
    create_bin_file(ofn, int_arr_to_bytes(res))

