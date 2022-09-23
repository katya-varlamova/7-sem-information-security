import sys
def create_bin_file(fn, info):
    with open(fn, "wb") as file:
        file.write(info)
def generate_binary(fn):
    s = "qwerty\n !@#$%^&*()_+-=uiop[]asdfgvhjhjkl;'\zxcv\n   bnm,./1234567890-=§/\n"
    create_bin_file(fn, s.encode('utf-8', 'big'))
if len(sys.argv) == 2:  
    generate_binary(sys.argv[1])
