### Warn when using join on a list of known literals. (join-literal)
```py
a = "foo"
b = "bar"
",".join([a, b])
```
Will be fixed to
```py
a = "foo"
b = "bar"
"{},{}".format(a, b)
```
### Use "yield from" instead of yield inside of a for loop (yield-from)
```py
seq = range(10)
for x in seq:
    yield x
```
Will be fixed to
```py
seq = range(10)
yield from seq
```
### Range len instead of enumerate (range-len)
```py
for i in range(len(sequence)):
    a = sequence[i]
    print(a)
```
Will be fixed to
```py
for i, a in enumerate(sequence):
    print(a)
```
### Move if to iterator (filter-iterator)
```py
for i in range(10):
    if i == 2:
        print(1)
        print(2)
```
Will be fixed to
```py
for i in (x for x in range(10) if x == 2):
    print(1)
    print(2)
```
### Flatten for-loops using nested comprehensions (nested-for)
```py
seq_a = [0]
seq_b = range(10)
for i in seq_a:
    for j in seq_b:
        print(i, j)
```
Will be fixed to
```py
seq_a = [0]
seq_b = range(10)
for i, j in ((i,j) for i in seq_a for j in seq_b):
    print(i, j)

```
