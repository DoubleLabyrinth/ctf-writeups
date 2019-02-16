#!/usr/bin/env python2
import re, sys
from pwn import *

def SendLine(m):
    conn.sendline(m)
    print(m)
    sleep(0.5)

conn = connect('hackme.inndy.tw', 7702)
sys.stdout.write(conn.read())
SendLine('43210')

while True:
    recv = conn.read()
    sys.stdout.write(recv)

    if recv.startswith('You are right') == False:
        a, b = re.match(r'\D*(\d+)\D*(\d+)\D*', recv).groups()
        SendLine('%d' % ((int(a) + int(b)) // 2))
    else:
        break

print(conn.readall())
