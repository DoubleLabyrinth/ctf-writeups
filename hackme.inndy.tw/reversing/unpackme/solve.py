#!/usr/bin/env python3

md5 = bytes.fromhex('34af0d074b17f44d1bb939765b02776f')
data = bytes.fromhex('1a8b24285837ac5253b51e3e4a254a276bb21701030bf41400f161700c55207a')

v = ord('h')
flag = bytearray(128)
for i in range(0, 32, 4):
    flag[i] = v ^ data[i] ^ md5[i % 16]
    flag[i + 1] = v ^ data[i + 1] ^ md5[(i + 1) % 16]
    flag[i + 2] = v ^ data[i + 2] ^ md5[(i + 2) % 16]
    flag[i + 3] = v ^ data[i + 3] ^ md5[(i + 3) % 16]

print(flag.strip(b'\x00').decode())

