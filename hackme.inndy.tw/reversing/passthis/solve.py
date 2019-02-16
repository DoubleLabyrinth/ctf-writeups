#!/usr/bin/env python3

key = 0x87
c = bytearray.fromhex('c1cbc6c0fcc9e8aba7dee8f2a7f4efe8f2ebe3a7e9e8f3a7f7e6f4f4a7f3efe2a7e1ebe6e0fa')
for i in range(len(c)):
    c[i] ^= key
print(c.decode())
