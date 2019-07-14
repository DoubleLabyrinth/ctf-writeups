#!/usr/bin/env python3

def XorBytes(a, b):
    assert(len(a) == len(b))
    return bytes([ i ^ j for i, j in zip(a, b) ])

answer = XorBytes(bytes.fromhex('1c0111001f010100061a024b53535009181c'), bytes.fromhex('686974207468652062756c6c277320657965'))
assert(answer == bytes.fromhex('746865206b696420646f6e277420706c6179'))

print(answer.hex())
