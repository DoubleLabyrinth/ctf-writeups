#!/usr/bin/env python3
import sys, os

def PrintBytes(bs):
    for i in range(0, len(bs), 16):
        print(' '.join(['%.2x' % b for b in bs[i:i + 16]]))

def GenerateSBox(iv: bytes):
    assert (len(iv) == 8)
    sbox = bytearray([i for i in range(256)])
    for i in range(8):
        sbox = UpdateSBox(sbox, iv[i], i)
    return bytes(sbox)

def UpdateSBox(sbox: bytearray, key_byte : int, index : int):
    x = key_byte & 0xff
    y = index & 0xff
    for _ in range(36):
        # y = (13 * (y ^ 0xffffffff)) & 0xff
        # x = (17 * (x ^ 0xffffffff)) & 0xff
        y = (13 * (~y)) & 0xff
        x = (17 * (~x)) & 0xff
        sbox[x], sbox[y] = sbox[y], sbox[x]
    return sbox

def Encrypt(plaintext : bytes, sbox : bytes, password : bytes):
    assert(len(sbox) == 256)

    sbox = bytearray(sbox)
    ciphertext = bytearray(len(plaintext))

    for i in range(len(plaintext)):
        sbox = UpdateSBox(sbox, password[i % len(password)], i % len(password))
        k = 0xdeadbeef
        for j in range(256):
            k = (0xC8763 * sbox[j] ^ 0x5A77 * k) & 0xffffffff
        ciphertext[i] = ((17 * plaintext[i]) ^ k) & 0xff
    
    return bytes(ciphertext)

def Decrypt(ciphertext : bytes, sbox : bytes, password : bytes):
    assert(len(sbox) == 256)

    sbox = bytearray(sbox)
    plaintext = bytearray(len(ciphertext))

    for i in range(len(ciphertext)):
        sbox = UpdateSBox(sbox, password[i % len(password)], i % len(password))
        k = 0xdeadbeef
        for j in range(256):
            k = (0xC8763 * sbox[j] ^ 0x5A77 * k) & 0xffffffff
        plaintext[i] = (ciphertext[i] ^ (k & 0xff)) * 241 % 256
    
    return bytes(plaintext)

def help():
    print('Usage:')
    print('    ./rc87cipher.py <enc|dec> <input file> <output file> <password>')
    print()

def main(argc : int, argv : list):
    if argc != 5:
        help()
        return
    else:
        if argv[1].lower() == 'enc':
            with open(argv[2], 'rb') as f:
                plaintext_bytes = f.read()
            
            iv = os.urandom(8)
            sbox = GenerateSBox(iv)

            print('Your IV:')
            PrintBytes(iv)
            print('Your SBox:')
            PrintBytes(sbox)

            ciphertext_bytes = Encrypt(plaintext_bytes, sbox, argv[4].encode())

            with open(argv[3], 'wb') as f:
                f.write(ciphertext_bytes)
        elif argv[1].lower() == 'dec':
            with open(argv[2], 'rb') as f:
                ciphertext_bytes = f.read()

            iv, ciphertext_bytes = ciphertext_bytes[:8], ciphertext_bytes[8:]
            sbox = GenerateSBox(iv)

            print('Your IV:')
            PrintBytes(iv)
            print('Your SBox:')
            PrintBytes(sbox)

            plaintext_bytes = Decrypt(ciphertext_bytes, sbox, argv[4].encode())

            with open(argv[3], 'wb') as f:
                f.write(plaintext_bytes)
        else:
            help()
            return
        
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

