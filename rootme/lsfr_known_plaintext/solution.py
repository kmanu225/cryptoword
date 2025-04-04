import os

keystream = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0] + [0] * 2000000

for i in range(16, 2000000):
    keystream[i] = (
        keystream[i - 1] ^ keystream[i - 3] ^ keystream[i - 11] ^ keystream[i - 16]
    )
p = open(os.path.dirname(__file__) + "\ch32\challenge.png", "wb")

Cipher = open(os.path.dirname(__file__) + "\ch32\challenge.png.encrypt", "rb").read()
idx = 0
for c in Cipher:
    k = 0
    for i in range(8):
        k <<= 1
        k = k | keystream[idx]
        idx += 1
    #  print(c^k)
    p.write(bytes([c ^ k]))
p.close()
