# hackme.inndy.tw --- reversing --- 2018-rev

## 1. Challenge

```
Happy New Year 2018! Can you execute this binary on the right time with the right argv?
```

## 2. Solution

```
$ gcc solve.c -o solve
$ sudo date -s '2018/1/1 00:00:00' -u && ./solve ./2018.rev && sudo systemctl restart systemd-timesyncd
```


