import random
import sys
c0 = [57, 49, 41, 33, 25, 17 ,9, 1, 58, 50, 42, 34, 26, 18 ,10, 2, 59, 51 ,43, 35, 27, 19, 11, 3 ,60, 52 ,44, 36]
d0 = [63, 55, 47, 39, 31, 23 ,15 ,7, 62, 54, 46, 38, 30, 22, 14, 6 ,61 ,53, 45, 37 ,29 ,21 ,13 ,5 ,28 ,20 ,12, 4]
shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
compress = [ 14, 17 ,11 ,24 ,1, 5, 3, 28, 15 ,6 ,21, 10, 23 ,19, 12, 4, 26 ,8 ,16, 7, 27 ,20 ,13 ,2 ,
             41 ,52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34 ,53 ,46 ,42 ,50 ,36 ,29 ,32]
ip = [58, 50, 42, 34, 26, 18, 10, 2,
60, 52 ,44, 36, 28 ,20, 12, 4,
62 ,54, 46, 38, 30, 22, 14, 6,
64, 56, 48 ,40 ,32 ,24, 16, 8,
57,49,41,33,25,17,9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7]

ipt = [40,8 ,48 ,16,56,24,64,32,
       39,7, 47, 15,55,23,63,31,
       38, 6 ,46, 14 ,54,22,62,30,
       37,5 ,45, 13,53,21,61,29,
       36,4, 44, 12,52,20,60,28,
       35,3, 43, 11,51,19,59,27,
       34,2, 42, 10,50,18,58,26,
       33,1, 41,9,49,17,57,25]
ext = [32, 1, 2, 3, 4, 5,
       4, 5, 6, 7, 8, 9,
       8, 9, 10, 11, 12, 13,
       12, 13, 14, 15, 16, 17,
       16, 17, 18, 19, 20, 21,
       20, 21, 22, 23, 24, 25,
       24, 25, 26, 27, 28, 29,
       28, 29, 30, 31, 32, 1]
p = [16, 7 ,20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2 ,8 ,24, 14, 32, 27, 3, 9 ,19, 13, 30, 6 ,22, 11, 4 ,25]
blocks  = []
def load_blocks(fn):
    global blocks
    with open(fn) as f:
        for line in f:
            arr = list(map(int, line.split()))
            block = []
            for i in range(4):
                block.append(arr[i * 16 : i * 16 + 16])
            blocks.append(block)
def load_key(fn):
    key = []
    with open(fn) as f:
        key = list(map(int, f.readline().split()))
    return key
          
for i in range(28):
    c0[i] -= 1
    d0[i] -= 1
for i in range(48):
    compress[i] -= 1
    ext[i] -= 1

for i in range(64):
    ip[i] -= 1
    ipt[i] -= 1
    
for i in range(32):
    p[i] -= 1
      
def shift_left(a):
    tmp = a[0]
    l = len(a)
    for i in range(l - 1):
        a[i] = a[i + 1]
    a[l - 1] = tmp
    return a
    
def generate_keys(key):
    first = []
    second = []
    rounds = []
    for i in range(28):
        first.append(0)
        second.append(0)
        
    # initial
    for i in range(28):
        first[i] = key[c0[i]]
        second[i] = key[d0[i]]
        
    # rounds
    for i in range(16):
        for j in range(shifts[i]):
            first = shift_left(first)
            second = shift_left(second)
        bc = first + second

        r = []
        for j in range(48):
            r.append(0)
        for j in range(48):
            r[j] = bc[compress[j]]
        rounds.append(r)
    return rounds
def xor(a1, a2):
    if len(a1) != len(a2):
        print("error")
        return
    res = []
    for i in range(len(a1)):
        res.append((a1[i] + a2[i]) % 2)
    return res
def feistel(msg, key):
    # extend
    res = []
    for i in range(48):
        res.append(0)
    for i in range(48):
        res[i] = msg[ext[i]]
    z = xor(res, key)
    res = []
    for i in range(8):
        
        row = z[i * 6] * 2 + z[i * 6 + 5]
        col = z[i * 6 + 1] * 8 + z[i * 6 + 2] * 4 + z[i * 6 + 3] * 2 + z[i * 6 + 4]
        val = blocks[i][row][col]
        tmp = [0, 0, 0, 0]
        j = 0
        while val > 0:
            tmp[3 - j] = val % 2
            val //= 2
            j += 1
        res += tmp
    r = []
    for i in range(32):
        r.append(0)
    for i in range(32):
        r[i] = res[p[i]]
    return r
    
def encrypt(msg, keys):
    # initial
    res = []
    for i in range(64):
        res.append(0)
    for i in range(64):
        res[i] = msg[ip[i]]

    # main
    left = res[:32]
    right = res[32:]
    for i in range(16):
        left_tmp = right
        right_tmp = xor(left, feistel(right, keys[i]))
        left = left_tmp
        right = right_tmp
        
    buf = left + right
    # finish
    for i in range(64):
        res[i] = buf[ipt[i]]
    return res

def decrypt(msg, keys):
    # initial
    res = []
    for i in range(64):
        res.append(0)
    for i in range(64):
        res[i] = msg[ip[i]]

    # main
    left = res[:32]
    right = res[32:]
    for i in range(15, -1, -1):
        right_tmp = left
        left_tmp = xor(right, feistel(left, keys[i]))
        left = left_tmp
        right = right_tmp
        
    buf = left + right
    
    # finish
    for i in range(64):
        res[i] = buf[ipt[i]]
        
    return res
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
def int_to_bits(i):
    res = [0, 0, 0, 0, 0, 0, 0, 0]
    j = 7
    while i > 0:
        res[j] = i % 2
        i //= 2
        j -= 1
    return res

def bits_to_int(arr):
    s = 0
    st = 1
    for i in range(len(arr)):
        s += arr[7 - i] * st
        st *= 2
    return s

def int_arr_to_bits64(i_arr, action):
    extra = 0
    if len(i_arr) % 8 != 0:
        extra = 8 - len(i_arr) % 8
        for i in range(extra):
            i_arr.append(0)
    bits = []
    bits_tmp = []
    for i in range(len(i_arr) ):
        if i > 0 and i % 8 == 0:
            bits.append(bits_tmp)
            bits_tmp = []
        bits_tmp += int_to_bits(i_arr[i])
    bits.append(bits_tmp)
    if action == 'e':
        with open("extra.txt", 'w') as f:
            print(extra, file=f)
    return bits

def bits64_to_int_arr(bits, action):
    i_arr = []
    for b in bits:
        for i in range(8):
            i_arr.append(bits_to_int(b[i * 8: i * 8 + 8]))
    if action == 'd':
        with open("extra.txt") as f:
            extra = int(f.read())
            i_arr = i_arr[:len(i_arr) - extra]
    return i_arr
def work(fn, action):
    arr = int_arr_to_bits64(bytes_to_int_arr(read_bin_file(fn)), action)
    
    key = load_key(sys.argv[1])
    keys = generate_keys(key)

    res = []
    for a in arr:
        if action == "e":
            c = encrypt(a, keys)
        if action == "d":
            c = decrypt(a, keys)
        res.append(c)
    create_bin_file(sys.argv[3], int_arr_to_bytes(bits64_to_int_arr(res, action)))
        

load_blocks("blocks.txt")
work(sys.argv[2], sys.argv[4])

