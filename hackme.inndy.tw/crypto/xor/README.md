# hackme.inndy.tw --- crypto --- xor

## 1. Challenge

```
I've X0Red some file, could you recover it?
```

## 2. Solution

```
$ pip install xortool

$ xortool ./xor
The most probable key lengths:
   1:   8.6%
   3:   10.6%
   6:   9.4%
   9:   21.8%
  12:   7.1%
  15:   6.2%
  18:   14.1%
  27:   9.7%
  36:   7.1%
  45:   5.4%
Key-length can be 3*n
Most possible char is needed to guess the key!

$ xortool ./xor -l 9 -c 20
1 possible key(s) of length 9:
hackmepls
Found 1 plaintexts with 95.0%+ printable characters
See files filename-key.csv, filename-char_used-perc_printable.csv
```

Go to see `./xortool_out/0.out` and you will find the flag.

Why do I use `-c 20`?

Because I think the space char `' '` is possible char in English text.

