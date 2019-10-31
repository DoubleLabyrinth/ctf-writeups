# hackme.inndy.tw --- reversing --- passthis

## 1. Challenge

```
You should be able to pass this
```

## 2. Solution

This is a challenge in windows. 

Drop the binary to IDA and you will find that it uses a XOR cipher and requires that the XOR result of the string you input and the string built in must be equal to `0x87` which is XOR key. 

```python
#!/usr/bin/env python3

key = 0x87
c = bytearray.fromhex('c1cbc6c0fcc9e8aba7dee8f2a7f4efe8f2ebe3a7e9e8f3a7f7e6f4f4a7f3efe2a7e1ebe6e0fa')
for i in range(len(c)):
    c[i] ^= key
print(c.decode())
```
