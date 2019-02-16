#!/usr/bin/env python3
import zlib

hashes = [
    0xd641596f,
    0x80a3e990,
    0xc98d5c9b,
    0x0d05afaf,
    0x1372a12d,
    0x5d5f117b,
    0x4001fbfd,
    0xa7d2d56b,
    0x7d04fb7e,
    0x2e42895e,
    0x61c97eb3,
    0x84ab43c3,
    0x9fc129dd,
    0xf4592f4d
]

i = 0
flag = bytearray()
while len(flag) != 42:
    found = False
    flag += b'\x00\x00\x00'
    for a in range(256):
        flag[-3] = a
        for b in range(256):
            flag[-2] = b
            for c in range(256):
                flag[-1] = c
                if hashes[i] == zlib.crc32(flag):
                    found = True
                    i += 1
                    break
            if found:
                break
        if found:
            break
    assert(found)
    print(flag)
print(flag.decode())

