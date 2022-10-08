import sys
import random
key = []
for i in range(64):
    key.append(random.randint(0, 1))
with open(sys.argv[1], 'w') as f:
    for i in range(64):
        f.write(str(key[i]) + ' ')
