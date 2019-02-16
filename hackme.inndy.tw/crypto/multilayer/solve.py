#!/usr/bin/env python3
import base64, re

def Xor(a, b):
    assert(len(a) == len(b))
    return bytes(i ^ j for i, j in zip(a, b))

with open('encrypted') as f:
    clues = f.read().split('\n')

n, e = re.match(r'RSA\(n=(.*), e=(.*)\)', clues[0]).groups()
n = int(n, 16)
e = int(e, 16)
RSA_Cipher_To_Plain = {}
for i in range(0, 256 * 256):
    m_bytes = b'%04x' % i
    m = int.from_bytes(m_bytes, 'big')
    c = pow(m, e, n)
    c_bytes = c.to_bytes(256, 'big')
    RSA_Cipher_To_Plain[c_bytes] = m_bytes

flag_sha256 = clues[1]

def DecryptLayer4(data):
    c = base64.b64decode(data)
    assert(len(c) % 256 == 0)

    m = b''
    while len(c) > 256:
        m = Xor(c[-512:-256], c[-256:]) + m
        c = c[:-256]
    assert(len(m) % 256 == 0)

    M = b''
    for i in range(0, len(m), 256):
        M += RSA_Cipher_To_Plain[m[i:i + 256]]

    return bytes.fromhex(M.decode())

def DecryptLayer3And2(data):
    for key in range(0, 256):
        keys = bytearray()
        for i in range(len(data)):
            key = (key * 0xc8763 + 9487) % 0x10000000000000000
            keys.append(key & 0xff)
        m = Xor(data, keys)
        m = bytes([ m[i] * 192 % 251 for i in range(len(m)) ])
        if m[4] == ord('{') and m.endswith(b'}\n'):
            return m
    return None

flag = clues[3]
flag = DecryptLayer4(flag)
flag = DecryptLayer3And2(flag)

print(flag.decode())
print('Go to https://quipqiup.com/ to solve layer1, with clue \'SKIT=FLAG\'')
