#: Use "yield from" instead of yield inside of a for loop
# yield-from
seq = range(10)
for x in seq:
    yield x
# ==>
seq = range(10)
yield from seq
