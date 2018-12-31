# noqa: F821
#: Range len instead of enumerate
# range-len
seq = [0]
for i in range(len(seq)):
    a = seq[i]
    print(a)
# ==>
seq = [0]
for i, a in enumerate(seq):
    print(a)
#: Replace an empty body with pass
# range-len
seq = [0]
for i in range(len(seq)):
    a = seq[i]
# ==>
seq = [0]
for i, a in enumerate(seq):
    pass
#: As seen on the README
# range-len
for i in range(len(sequence)):
    x = sequence[i]
    do_thing(x, i)
# ==>
for i, x in enumerate(sequence):
    do_thing(x, i)
