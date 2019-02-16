#!/usr/bin/env python3

with open('plain.txt') as f:
    plain = f.read()
with open('crypted.txt') as f:
    crypted = f.read()

statistic_plain = {}
for c in plain:
    if statistic_plain.get(c) == None:
        statistic_plain[c] = 1
    else:
        statistic_plain[c] += 1

statistic_crypted = {}
for c in crypted:
    if statistic_crypted.get(c) == None:
        statistic_crypted[c] = 1
    else:
        statistic_crypted[c] += 1

p = ''
c = ''

for k1 in statistic_plain.keys():
    matches = []
    for k2 in statistic_crypted.keys():
        if statistic_plain[k1] == statistic_crypted[k2]:
            matches.append(k2)
    if (len(matches) == 1):
        p += k1
        c += matches[0]
    else:
        # some hints
        if k1 == 'P':
            p += k1
            c += 'y'
        elif k1 == 'q':
            p += k1
            c += 'i'
        elif k1 == 'W':
            p += k1
            c += '<'
        elif k1 == '{':
            p += k1
            c += '#'
        elif k1 == '}':
            p += k1
            c += 'K'
        elif k1 == 'M':
            p += k1
            c += '~'
        else:
            print('Unsolved: %c -> { %s }' % (k1, ' '.join(matches)))

T = str.maketrans(c, p)

print()
print('******************************')
print('*         Plaintext          *')
print('******************************')
print(crypted.translate(T))

