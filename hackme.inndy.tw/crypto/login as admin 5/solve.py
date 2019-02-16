#!/usr/bin/env python3
import base64, urllib.parse, requests

def Xor(a, b):
    assert(len(a) == len(b))
    return bytes([ i ^ j for i, j in zip(a, b) ])

p = b'{"name":"guest","admin":false}'
c = base64.b64decode(urllib.parse.unquote('U%2FosUbnY8nSrWz4WPwKSwWPzKq9tOIQ9eCWnN5E%2B'))
key = Xor(p, c)

new_p = b'{"name":"admin", "admin":true}'
new_c = Xor(new_p, key)

r = requests.get('https://hackme.inndy.tw/login5/',
                 cookies = { 'user5' : urllib.parse.quote(base64.b64encode(new_c).decode()) })
print(r.text)

