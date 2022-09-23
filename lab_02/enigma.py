import random
import sys
    
class Reflector:
    def __init__(self, seq):
        self.seq = seq
        self.size = len(seq)
    def get_seq(self):
        return self.seq
    
class Rotor:
    def __init__(self, seq):
        self.seq = seq
        self.shift = 0
        self.size = len(seq)
    def get_seq(self):
        return self.seq
    def __shift_seq(self, a):
        tmp1 = a[0]
        l = len(a)
        for i in range(l):
            tmp2 = a[(i + 1) % l]
            a[(i + 1) % l] = tmp1
            tmp1 = tmp2
        return a
    def turn(self):
        self.shift += 1
        self.seq = self.__shift_seq(self.seq)
        if self.shift == self.size:
            self.shift = 0
            return True
        return False
    def clone(self):
        cR = Rotor(1)
        cR.shift = self.shift
        cR.size = self.size
        cR.seq = []
        for i in range(len(self.seq)):
            cR.seq.append(self.seq[i])
        return cR
        

class RotorSystem:
    def __init__(self, seqs):
        self.rotors = []
        for i in range(len(seqs)):
            self.rotors.append(Rotor(seqs[i]))
    def getRotorCount(self):
        return len(self.rotors)
    def getRotor(self, ind):
        return self.rotors[ind]
    def turn(self):
        i = 0
        while self.rotors[i].turn() and i < len(self.rotors):
            i += 1
    def clone(self):
        cRS = RotorSystem(1, 1)
        cRS.rotors = []
        for i in range(len(self.rotors)):
            cRS.rotors.append(self.rotors[i].clone())        
        return cRS

class Enigma:
    def __init__(self, rs, refl):
        self.system = rs
        self.refl = refl
    def work(self, seq):
        rseq = []
        for s in seq:
            self.system.turn()
            ## direct
            n = s
            for i in range(self.system.getRotorCount()):
                n = self.system.getRotor(i).get_seq()[n]
                
            ## reflection
            n = self.refl.get_seq()[n]
            
            ## indirect
            for i in range(self.system.getRotorCount() - 1, -1, -1):
                for j in range(len(self.system.getRotor(i).get_seq())):
                    if n == self.system.getRotor(i).get_seq()[j]:
                        n = j
                        break
            rseq.append(n)
        return rseq

def read_config(fn):
    arr = []
    with open(fn, "r") as file:
        for line in file:
            arr.append(list(map(int, line.split())))
    return arr

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
    
def bytes_encryption(conf, fn, fn_enc):
    size = 256

    arr = read_config(conf)
    rs = RotorSystem(arr[1:])
    reflector = Reflector(arr[0])

    i_arr = bytes_to_int_arr(read_bin_file(fn))
    enigma_enc = Enigma(rs, reflector)
    enc_i_seq = enigma_enc.work(i_arr)
    create_bin_file(fn_enc, int_arr_to_bytes(enc_i_seq))


if len(sys.argv) == 4:
    bytes_encryption(sys.argv[1], sys.argv[2], sys.argv[3])
    
