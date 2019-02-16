#!/usr/bin/env python3

data = bytes.fromhex('8faa85a048ac4095b616be40b41697b1bebc16b1bc169d95bc4116364295951640b1beb21636423d3d49')

flag = bytearray()
for i in range(len(data)):
    c = (((data[i] & 0xAA) >> 1) & 0xff) | ((2 * (data[i] & 0x55)) & 0xff)
    flag.append(c - 9)
print(flag.decode())

