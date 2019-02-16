#!/usr/bin/env python2
from pwn import *

conn = connect('hackme.inndy.tw', 7700)

recv = conn.readuntil('(Press any key to continue)\n')
c = recv.split('\n')[-4]
print('encrypted_flag = %s' % c)
c = c.decode('hex')

cs = []
while True:
    try:
        conn.sendline();
        recv = conn.readuntil('(Press any key to continue)\n').split('\n')[0]
        print('%4d -> %s' % (len(cs), recv))
        cs.append(recv.decode('hex'))
    except EOFError:
        break
sample_count = len(cs)

key = bytearray(32)
for i in range(32):
    b0 = 0
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    for j in range(len(cs)):
        if ord(cs[j][i]) & 0x01:
            b0 += 1
        if ord(cs[j][i]) & 0x02:
            b1 += 1
        if ord(cs[j][i]) & 0x04:
            b2 += 1
        if ord(cs[j][i]) & 0x08:
            b3 += 1
        if ord(cs[j][i]) & 0x10:
            b4 += 1
    k = 0b01100000 ^ (ord(cs[0][i]) & 0b11100000)
    k |= 0x04 if b2 > sample_count // 2 else 0x00
    k |= 0x08 if b3 > sample_count // 2 else 0x00
    k |= 0x10 if b4 > sample_count // 2 else 0x00
    print ' '.join([ str(b0), str(b1), str(b2), str(b3), str(b4) ]), '->', '0x%02x 0x%02x 0x%02x 0x%02x' % (k, k + 1, k + 2, k + 3)
    key[i] = k

assert(len(c) == len(key))
print('encrypted_flag = %s' % c.encode('hex'))
print('Possible chars:')
for i in range(len(key)):
    cv = ord(c[i])
    print ('flag[%d]' % i).ljust(8, ' '), '=', ' '.join([ repr(chr(cv ^ (key[i] + j))) for j in range(4) ])


