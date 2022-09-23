import random
import sys
def create_config(fn, count, size):
    with open(fn, "w") as file:
        
        half = random.sample(range(size // 2, 2 * (size // 2)), size // 2)
        seq = [i for i in half]
        for c in range(size // 2, 2 * (size // 2)):
            for i in range(len(half)):
                if half[i] == c:
                    seq.append(i)
        if size % 2 != 0:
            seq.append(size - 1)
        file.write(" ".join(list(map(str, seq)))  + '\n')

        for i in range(count):
            file.write(" ".join(list(map(str, random.sample(range(0,size), size))))  + '\n')
def read_config(fn):
    arr = []
    with open(fn, "r") as file:
        for line in file:
            arr.append(list(map(int, line.split())))
    return arr

if len(sys.argv) == 4:
    create_config(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

