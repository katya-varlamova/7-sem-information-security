import sys
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def create_bin_file(fn, info):
    with open(fn, "wb") as file:
        file.write(info)
def generate_binary(fn):
    s = "qwerty\n !@#$%^&*()_+-=uiop[]asdfgvhjhjkl;'\zxcv\n   bnm,./1234567890-=§/\n"
    s += randomword(20)
    create_bin_file(fn, s.encode('utf-8', 'big'))
if len(sys.argv) == 2:  
    generate_binary(sys.argv[1])
