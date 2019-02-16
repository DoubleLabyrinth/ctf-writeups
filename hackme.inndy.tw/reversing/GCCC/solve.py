#!/usr/bin/env python3

space = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ{} '

array = bytearray([
    164, 25, 4, 130,
    126, 158, 91, 199,
    173, 252, 239, 143,
    150, 251, 126, 39,
    104, 104, 146, 208,
    249, 9, 219, 208,
    101, 182, 62, 92,
    6, 27, 5, 46
])

b = 0
for i in range(len(array)):
    array[i] ^= b
    b = array[i]

key = array[0] ^ ord('F')
flag = bytearray(b'FLAG{**************************}')
assert(len(flag) == 32)

assert(flag[0] != ord('*'))
for i in range(1, 32):
    if (flag[i] != ord('*')):
        k1 = array[i] ^ flag[i]
        k2 = key >> i
        assert((k1 & 0x7F) == (k2 & 0x7F))
        key |= k1 << i
    else:
        k1 = ((key >> i) & 0x7F) | (array[i] & 0x80)
        assert((k1 ^ array[i]) in space)
        flag[i] = array[i] ^ k1
        key |= k1 << i

print('key = %d' % key)
print(flag.decode())
