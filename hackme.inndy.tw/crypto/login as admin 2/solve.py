#!/usr/bin/env python3
import hashpumpy, requests, base64

# login as guest
user_cookie = 'NmJjYjljOTE1NTk3NWE1M2U5NTFiMGI1MGYxMzc0ODAjbmFtZT1ndWVzdCZhZG1pbj0w'

sig, serial = base64.b64decode(user_cookie).decode().split('#')
new_sig, new_serial = hashpumpy.hashpump(sig, serial.encode(), '&admin=1', len(sig))
new_cookie = base64.b64encode(new_sig.encode() + b'#' + new_serial).decode()

r = requests.get('https://hackme.inndy.tw/login2/', cookies = { 'user' : new_cookie })
print(r.text)

