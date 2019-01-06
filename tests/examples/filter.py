#: Move if to iterator
# filter-iterator
for i in range(10):
    if i == 2:
        print(1)
        print(2)
# ==>
for i in (x for x in range(10) if x == 2):
    print(1)
    print(2)
# END
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
# END
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
# END
#: Merge into existing expr
# filter-iterator
for i in (a * 2 for a in range(2)):
    if pred(i):
        pass
# ==>
for i in (a * 2 for a in range(2) if pred(a * 2)):
    pass

# END
#: Merge into existing complex expr
# filter-iterator
for i in (f(a) * 2 for a in range(2)):
    if pred(i):
        pass
# ==>
for i in (f(a) * 2 for a in range(2) if pred(f(a) * 2)):
    pass
# END
