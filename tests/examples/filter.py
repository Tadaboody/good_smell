#: Move if to iterator if
# filter-iterator
for i in range(10):
    if i == 2:
        print(1)
        print(2)
# ==>
for i in (x for x in range(10) if x == 2):
    print(1)
    print(2)
#: Don't move if there's code before
# None
for i in range(10):
    print(1)
    if pred(i):
        print(2)
# ==>
for i in range(10):
    print(1)
    if pred(i):
        print(2)
#: don't move if there's code after
# None
for i in range(10):
    if pred(i):
        print(1)
    print(2)
# ==>
for i in range(10):
    if pred(i):
        print(1)
    print(2)
