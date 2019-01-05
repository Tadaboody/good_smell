#: use yield from iter instead for x in iter -> yield x
# yield-from
def test1():
    seq = range(10)
    for x in seq:
        yield x
test1()
# ==>
def test2():
    seq = range(10)
    yield from seq
test2()