#: Use itertools instead of nsted fors
# nested-for
seq_a = [0]
seq_b = range(10)
for i in seq_a:
    for j in seq_b:
        print(i, j)
# ==>
import itertools
seq_a = [0]
seq_b = range(10)
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
#: Don't flatten a nested for with dependencies (#26)
# None
for num in range(1, 5):
    for digits in range(1, 10 ** num):
        pass
# ==>
for num in range(1, 5):
    for digits in range(1, 10 ** num):
        pass
