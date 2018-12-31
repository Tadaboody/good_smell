# noqa: F821
# flake8: noqa
# pylint: disable=consider-using-enumerate,undefined-variable
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
#: replaces access
# range-len
for i in range(len(sequence)):
    other_thing(sequence[i], i)
# ==>
for i, elm in enumerate(sequence):
    other_thing(elm, i)
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
    for j, _ in enumerate(sequence):
        do_thing(x, j)
    other_thing(x, i)
#: Replace unused var with _
# range-len
for i in range(len(sequence)):
    do_thing(i)
# ==>
for i, _ in enumerate(sequence):
    do_thing(i)
#: Don't remove an assign to something else
# range-len
for i in range(len(sequence)):
    a = 0
    print(sequence[j])
# ==>
for i, _ in enumerate(sequence):
    a = 0
    print(sequence[j])
