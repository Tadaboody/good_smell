#: Flatten for-loops using nested comprehensions
# nested-for
seq_a = [0]
seq_b = range(10)
for i in seq_a:
    for j in seq_b:
        print(i, j)
# ==>
seq_a = [0]
seq_b = range(10)
for i, j in ((i,j) for i in seq_a for j in seq_b):
    print(i, j)

# END
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
# END
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
# END
#: Don't flatten a nested for with dependencies (#26)
# None
for num in range(1, 5):
    for digits in range(1, 10 ** num):
        pass
# ==>
for num in range(1, 5):
    for digits in range(1, 10 ** num):
        pass
#: Check no errors with unpacking (#61)
# None
for i, num in enumerate(range(1, 5)):
    for digits in range(1, 10 ** num):
        pass
# ==>
for i, num in enumerate(range(1, 5)):
    for digits in range(1, 10 ** num):
        pass
