#!/usr/bin/env python3
import requests

space = { i for i in range(256) }
statistics = { i : {} for i in range(50) }

while True:
    r = requests.get('https://hackme.inndy.tw/otp/', { 'issue_otp' : 'show' })
    cs = r.text.split('\n')

    for i in range(20):
        cs[i] = bytes.fromhex(cs[i])
        assert (len(cs[i]) == 50)

    for i in range(20):
        for j in range(50):
            statistics[j][cs[i][j]] = 1

    print(''.join([ '%3d ' % len(statistics[i]) for i in range(50) ]))

    bContinue = False
    for i in range(50):
        if len(statistics[i]) != 255:
            bContinue = True

    if not bContinue:
        break

flag = bytearray()
for i in range(50):
    v = list(space - set(statistics[i].keys()))
    assert(len(v) == 1)
    flag.append(v[0])
print(flag.decode())
