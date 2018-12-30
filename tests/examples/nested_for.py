#: basic test
# nested-for
seq_a = [0]
seq_b = range(10)
for i in seq_a:
    for j in seq_b:
        print(i, j)
# ==>
seq_a = [0]
seq_b = range(10)
import itertools
for i, j in itertools.product(seq_a, seq_b):
    print(i, j)

#: Don't work if there's code between the loops (no way to know if it's unsafe)
# None
for i in seq_a:
    print(i)
    for j in seq_b:
        print(i, j)
# ==>
for i in seq_a:
    print(i)
    for j in seq_b:
        print(i, j)
#: Don't work if there's code after the nested for
# None
for i in seq_a:
    for j in seq_b:
        print(i, j)
    print(i)
# ==>
for i in seq_a:
    for j in seq_b:
        print(i, j)
    print(i)
