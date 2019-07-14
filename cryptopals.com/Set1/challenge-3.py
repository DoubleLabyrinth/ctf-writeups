#!/usr/bin/env python3

def XorSingleByte(m, k):
    c = bytearray(m)
    for i in range(len(c)):
        c[i] ^= k
    return bytes(c)

c = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
print('Possible answers:')
for k in range(0, 256):
    m = XorSingleByte(c, k)
    try:
        m = m.decode('ascii')
    except:
        continue
    if m.isprintable():
        print(m)

print()
print('Find the most readable one. :-)')
