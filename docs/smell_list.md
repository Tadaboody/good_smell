### Range len instead of enumerate (range-len)
```py
seq = [0]
for i in range(len(seq)):
    a = seq[i]
    print(a)

```
Will be fixed to
```py
seq = [0]
for i, a in enumerate(seq):
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
### Use itertools instead of nsted fors (nested-for)
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
import itertools
for i, j in itertools.product(seq_a, seq_b):
    print(i, j)

```
