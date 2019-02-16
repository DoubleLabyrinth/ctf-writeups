#!/usr/bin/env python3

def GetKeySpace(k):
    values = bytearray()
    values.append(k % 256)
    while True:
        k = (0x777777 * k + 12345) & 0x7FFFFFFFFFFFFFFF
        if k % 256 != values[0]:
            values.append(k % 256)
        else:
            break
    return bytes(values)

def DecryptWithKey(c, k):
    t = 7
    m = bytearray(c)
    ks = GetKeySpace(k)
    ki = 0
    for i in range(len(m)):
        ki = (ki + t) % len(ks)
        m[i] = m[i] ^ ks[ki]
        t = ((21 * t & 0xffffffffffffffff) // 10) ^ m[i]
    return bytes(m)

with open('flag.enc', 'rb') as f:
    flag_enc = f.read()

flag_7z = DecryptWithKey(flag_enc, 49)

with open('flag.7z', 'wb') as f:
    f.write(flag_7z)
