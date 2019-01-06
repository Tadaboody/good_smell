#: use yield from iter instead for x in iter -> yield x
# yield-from
seq = range(10)
for x in seq:
    yield x
# ==>
seq = range(10)
yield from seq
