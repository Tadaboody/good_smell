# noqa: F821
# flake8: noqa
#pylint: disable=consider-using-enumerate,undefined-variable
sequence = []
#: Range len instead of enumerate
# range-len
sequence = [0]
for i in range(len(sequence)):
    a = sequence[i]
    print(a)
# ==>
sequence = [0]
for i, a in enumerate(sequence):
    print(a)
#: Replace an empty body with pass
# range-len
sequence = [0]
for i in range(len(sequence)):
    a = sequence[i]
# ==>
sequence = [0]
for i, a in enumerate(sequence):
    pass
#: Multiple replaces
# range-len
for i in range(len(sequence)):
    x = sequence[i]
    do_thing(x, i)
    other_thing(sequence[i], i)
# ==>
for i, x in enumerate(sequence):
    do_thing(x, i)
    other_thing(x, i)

#: Nested for
# range-len
for i in range(len(sequence)):
    x = sequence[i]
    for j in range(len(sequence)):
        do_thing(x, j)
    other_thing(sequence[i], i)
# ==>
for i, x in enumerate(sequence):
    for j, elm in enumerate(sequence):
        do_thing(x, j)
    other_thing(x, i)
