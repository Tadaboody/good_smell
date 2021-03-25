#: Range len instead of enumerate
# range-len
for i in range(len(sequence)):
    a = sequence[i]
    print(a)
# ==>
for i, a in enumerate(sequence):
    print(a)
# END
#: Replace an empty body with pass
# range-len
for i in range(len(sequence)):
    a = sequence[i]
# ==>
for i, a in enumerate(sequence):
    pass
# END
#: replaces access
# range-len
for i in range(len(sequence)):
    other_thing(sequence[i], i)
# ==>
for i, elm in enumerate(sequence):
    other_thing(elm, i)
# END
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

# END
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
# END
#: Replace unused var with _
# range-len
for i in range(len(sequence)):
    do_thing(i)
# ==>
for i, _ in enumerate(sequence):
    do_thing(i)
# END
#: Don't remove an assign to something else
# range-len
for i in range(len(sequence)):
    a = 0
    print(sequence[j])
# ==>
for i, _ in enumerate(sequence):
    a = 0
    print(sequence[j])
# END
#: Behave correctly when used in the upper part of a slice
# range-len
for i in range(len(sequence)):
    print(sequence[1:i])
# ==>
for i, _ in enumerate(sequence):
    print(sequence[1:i])
# END
#: Don't replace access when used in the upper part of a slice
# range-len
for i in range(len(sequence)):
    print(sequence[i:1])
# ==>
for i, _ in enumerate(sequence):
    print(sequence[i:1])
# END
#: Don't replace access used in the upper part of a slice
# range-len
for i in range(len(sequence)):
    print(sequence[2:1])
# ==>
for i, _ in enumerate(sequence):
    print(sequence[2:1])
# END