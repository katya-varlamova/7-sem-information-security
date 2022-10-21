import sys
import rsa
def generate_keys():
    ekey, dkey = rsa.newkeys(1024)
    return (ekey, dkey)
def create_bin_file(fn, info):
    with open(fn, "wb") as file:
        file.write(info)

def read_bin_file(fn):
    with open(fn, "rb") as file:
        return file.read()


def create_signature(dkey, obj):
    return rsa.sign(obj, dkey, 'SHA-256')

def check_signature(sig, ekey, obj):
    try:
        rsa.verify(obj, sig, ekey)
        return True
    except Exception:
        return False


if len(sys.argv) < 2:
    exit(0)
    
if sys.argv[1] == '-g':
    e, d = generate_keys()
    with open("key.pub", 'w') as f:
        print('{} {}'.format(e.e, e.n), file = f)
    with open("key.pri", 'w') as f:
        print('{} {} {} {} {}'.format(e.n, e.e, d.d, d.p, d.q), file = f)
        
if sys.argv[1] == '-s':
    ifn = sys.argv[2]
    ofn = sys.argv[3]
    d = 0
    p = 0
    q = 0
    e = 0
    n = 0
    with open("key.pri") as f:
        n, e, d, p, q = map(int, f.readline().split())
        
    dkey = rsa.PrivateKey(n=n, e=e, d=d, p=p, q=q)
    sig = create_signature(dkey, read_bin_file(ifn))
    create_bin_file(ofn, sig)


if sys.argv[1] == '-c':
    ifn = sys.argv[2]
    sfn = sys.argv[3]
    e = 0
    n = 0
    with open("key.pub") as f:
        e, n = map(int, f.readline().split())
    ekey = rsa.PublicKey(e=e, n=n)
    
    obj = read_bin_file(ifn)
    sig = read_bin_file(sfn)
    print(check_signature(sig, ekey, obj))
    
  
