# hackme.inndy.tw --- crypto --- easy AES

## 1. Challenge

```
Can you encrypt things with AES?
Tips: What is symmetric cipher?
```

## 2. Solution

According to the python3 script `what-is-aes.py`, we can know we must find the corresponding plaintext of the following ciphertext:

```
b'Good Plain Text!'
```

with cipher algorithm AES-128 and key `b'Hello, World...!'`.

It is easy to find:

```python
c = AES.new(b'Hello, World...!', AES.MODE_ECB)
m = c.decrypt(b'Good Plain Text!')  # m is b'bL\x15\xd8\x08EG2s\x91t3E\x98Le'
print(m.hex())                      # the hex string of m is '624c15d8084547327391743345984c65'
```

Then run `what-is-aes.py` with `624c15d8084547327391743345984c65` as input and you will get a picture.

Open the picture, and you will see the flag is

```
FLAG{I can encrypt AES}
```

