# hackme.inndy.tw --- crypto --- ffa

## 1. Challenge

```
finite field arithmetic
```

ffa.py
```python
#!/usr/bin/env python3
import sympy
import json

m = sympy.randprime(2**257, 2**258)
M = sympy.randprime(2**257, 2**258)
a, b, c = [(sympy.randprime(2**256, 2**257) % m) for _ in range(3)]

x = (a + b * 3) % m
y = (b - c * 5) % m
z = (a + c * 8) % m

flag = int(open('flag', 'rb').read().strip().hex(), 16)
p = pow(flag, a, M)
q = pow(flag, b, M)

json.dump({ key: globals()[key] for key in "Mmxyzpq" }, open('crypted', 'w'))
```

crypted
```
{"p": 240670121804208978394996710730839069728700956824706945984819015371493837551238, "q": 63385828825643452682833619835670889340533854879683013984056508942989973395315, "M": 349579051431173103963525574908108980776346966102045838681986112083541754544269, "z": 213932962252915797768584248464896200082707350140827098890648372492180142394587, "m": 282832747915637398142431587525135167098126503327259369230840635687863475396299, "x": 254732859357467931957861825273244795556693016657393159194417526480484204095858, "y": 261877836792399836452074575192123520294695871579540257591169122727176542734080}
```

## 2. Solution

We can know that `x`, `y`, `z`, `m`, `p`, `q`, `M` is given.

First, let's try to find `a`, `b`, `c` out. Based on the code in `ffa.py`, we can know there is a equation:

```
-----   ----------   -----
| x |   | 1 3 0  |   | a |
| y | = | 0 1 -1 | * | b |
| z |   | 1 0 8  |   | c |
-----   ----------   -----
```

over finite field GF(m).

We can use __SageMath__ to solve this equation:

```
A = MatrixSpace(GF(m), 3, 3)([[1, 3, 0], [0, 1, -5], [1, 0, 8]])
B = MatrixSpace(GF(m), 3, 1)([[x], [y], [z]])
X = A.inverse() * B

a, b, c = int(X[0, 0]), int(X[1, 0]), int(X[2, 0])
```

With `a`, `b`, `c` known, calculate `i = a ^ -1 (mod phi(M))`.

```python
phi_M = M - 1
g, i, j = xgcd(a, phi_M)
while a < 0:
    i += phi_M
assert(g == 1)
```

Calulate `flag = pow(p, i, M)` to get the flag.

