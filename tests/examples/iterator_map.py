#: Transformation can be moved to iterator
# iterator-map
for i in range(10):
    print(f(i))
    b = f(i)
# ==>
for i in (f(x) for x in range(10)):
    print(i)
    b = i
