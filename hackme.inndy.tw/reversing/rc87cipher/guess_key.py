#!/usr/bin/env python3

def GenerateSBox(IV: bytes):
    assert (len(IV) == 8)
    sbox = bytearray([i for i in range(256)])
    for i in range(8):
        sbox = UpdateSBox(sbox, IV[i], i)
    return sbox

def UpdateSBox(sbox: bytearray, key, index):
    x = key & 0xff
    y = index & 0xff
    for _ in range(36):
        # y = (13 * (y ^ 0xffffffff)) & 0xff
        # x = (17 * (x ^ 0xffffffff)) & 0xff
        y = (13 * (~y)) & 0xff
        x = (17 * (~x)) & 0xff
        sbox[x], sbox[y] = sbox[y], sbox[x]
    return sbox

def GuessOneKeyByte(plaintext, ciphertext, sbox, index, key_length):
    assert(len(plaintext) == len(ciphertext))
    assert(index < len(plaintext))
    assert(index < key_length)

    possible_key_bytes = []
    mask_key = ((17 * plaintext[index]) & 0xff) ^ ciphertext[index]

    for key_byte in range(0x20, 0x7f):
        next_sbox = UpdateSBox(sbox.copy(), key_byte, index)
        k = 0xdeadbeef
        for i in range(256):
            k = (0xC8763 * next_sbox[i] ^ 0x5A77 * k) & 0xffffffff
        if k & 0xff == mask_key:
            possible_key_bytes.append(key_byte)

    return possible_key_bytes

def GuessKey(plaintext, ciphertext, sbox, known_key_bytes, key_length):
    assert(len(known_key_bytes) <= key_length)
    if len(known_key_bytes) == key_length:
        print(known_key_bytes.decode())
    else:
        possible_key_bytes = GuessOneKeyByte(plaintext, ciphertext, sbox, len(known_key_bytes), key_length)
        for k in possible_key_bytes:
            GuessKey(plaintext, ciphertext, UpdateSBox(sbox.copy(), k, len(known_key_bytes)), known_key_bytes + bytes([ k ]), key_length)

with open('rc87', 'rb') as f:
    p = f.read()
with open('rc87.enc', 'rb') as f:
    c = f.read()
assert (len(p) + 8 == len(c))

iv, c = c[:8], c[8:]
sbox = GenerateSBox(iv)
GuessKey(p, c, sbox, b'', 40)
