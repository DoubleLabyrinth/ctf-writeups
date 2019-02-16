# hackme.inndy.tw --- reversing --- helloworld

## 1. Challenge

```
Guess a number please :D
```

## 2. Solution

Drop the binary to IDA, and you will see 

![](pic0.png)

So, magic number is `314159265`

Run with the magic number and you will see the flag.

