# hackme.inndy.tw --- crypto --- not hard

## 1. Challenge

```
Nm@rmLsBy{Nm5u-K{iZKPgPMzS2I*lPc%_SMOjQ#O;uV{MM*?PPFhk|Hd;hVPFhq{HaAH<
Tips: pydoc3 base64
```

## 2. Solution

1. base85 decode -->

```
>>> base64.b85decode('Nm@rmLsBy{Nm5u-K{iZKPgPMzS2I*lPc%_SMOjQ#O;uV{MM*?PPFhk|Hd;hVPFhq{HaAH<')
b'IZGECR33IRXSA6LPOUQGW3TPO4QGEYLTMUZTEIDFNZRW6ZDJNZTT67I='
```

2. Base32 decode -->

```
>>> base64.b32decode('IZGECR33IRXSA6LPOUQGW3TPO4QGEYLTMUZTEIDFNZRW6ZDJNZTT67I=')
b'FLAG{Do you know base32 encoding?}'
```

