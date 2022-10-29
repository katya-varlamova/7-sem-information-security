import sys
def read_bin_file(fn):
    with open(fn, "rb") as file:
        return file.read()
    
def count_freq(msg):
    arr = []
    d = {}
    for s in msg:
        if s in d:
            d[s] += 1
        else:
            d[s] = 1
    for k in d:
        arr.append((d[k], k))
    return arr

    
def build_tree(frq):
    while len(frq) != 1:
        frq = sorted(frq, key=lambda x: x[0])
        a = frq[0]
        b = frq[1]
        frq=frq[2:]
        frq.append((a[0] + b[0], [a[1], b[1]] ))  
    return frq

def search_in_tree(tree, val):
    if type(tree[0]) == int:
        if val == tree[0]:
            return (True, [0])
    else:
        res_left = search_in_tree(tree[0], val)    
        if res_left[0] == True:
            return (True, [0] + res_left[1])

    if type(tree[1]) == int:
        if val == tree[1]:
            return (True, [1])
    else:
        res_right = search_in_tree(tree[1], val)
        if res_right[0] == True:
            return (True, [1] + res_right[1])

    return (False, [])

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

    
def frqs_to_bits(frq):
    bits = []
    m = frq[0][0]
    for i in range(len(frq)):
        if frq[i][0] > m:
            m = frq[i][0]
    bts = 0
    while m != 0:
        m //= 256
        bts += 1
        
    bits += int_to_bits(len(frq) - 1, 1)
    bits += int_to_bits(bts, 1)

    for i in range(len(frq)):
        bits += int_to_bits(frq[i][0], bts)
        bits += int_to_bits(frq[i][1], 1)
    return bits
    
def int_arr_to_bytes(i_arr):
    ba = bytearray()
    for i in i_arr:
        ba.append(i)
    return ba

def bits_to_int(arr, byte):
    s = 0
    st = 1
    for i in range(len(arr)):
        s += arr[byte * 8 - 1 - i] * st
        st *= 2
    return s

def int_arr_to_bytes(i_arr):
    ba = bytearray()
    for i in i_arr:
        ba.append(i)
    return ba

def encode(msg):
    frq = count_freq(msg)

    tree = build_tree(frq)[0][1]
    bits = []
    bits += frqs_to_bits(frq)
    
    for s in msg:
        res = search_in_tree(tree, s)
        if res[0] == False:
            return False
        else:
            bits += res[1]
    if len(bits) % 8 != 0:
        extrabits = []
        for k in range(8 - len(bits) % 8):
            extrabits.append(0)
        bits = int_to_bits(8 - len(bits) % 8, 1) + bits + extrabits

    i_arr = []
    for i in range(len(bits) // 8):
        i_arr.append(bits_to_int(bits[i * 8 : i * 8 + 8], 1))
    
    return int_arr_to_bytes(i_arr)
            
def decode(msg):
    extra = msg[0]
    l = msg[1] + 1
    bts = msg[2]

    frq = []
    for i in range(l):
        cur = msg[3 + i * (bts + 1) : 3 + i * (bts + 1) + bts + 1]
        bits = []
        for j in range(bts):
            bits += int_to_bits(cur[j], 1)
        count = bits_to_int(bits, bts)
        sym = cur[bts]
        frq.append((count, sym))

    tree = build_tree(frq)[0][1]
    
    msg = msg[3 + l * (bts + 1): ]

    bits = []
    for b in msg:
        bits += int_to_bits(b, 1)

    bits = bits[: len(bits) - extra]
    
    a = tree
    res = []
    if type(a) != int:
        for bit in bits:
            a = a[bit]
            if type(a) == int:
                res.append(a)
                a = tree

    return int_arr_to_bytes(res)

def create_bin_file(fn, info):
    with open(fn, "wb") as file:
        file.write(info)      

if sys.argv[1] == '-e':
    arr = read_bin_file(sys.argv[2])
    create_bin_file(sys.argv[3], encode(arr))


if sys.argv[1] == '-d':
    arr = read_bin_file(sys.argv[2])
    create_bin_file(sys.argv[3], decode(arr))

