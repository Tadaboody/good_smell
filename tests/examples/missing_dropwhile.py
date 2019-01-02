#: Move conditional continue to iterator using itertools.dropwhile
# missing-dropwhile
for x in iterable:
    # No body
    if pred(x):
        continue
    print(x)
# ==>
import itertools
for x in itertools.dropwhile(pred, iterable):
    print(x)

#: Create a lambda if needed
# missing-dropwhile
for x in iterable:
    # No body
    if x==2:
        continue
    print(x)

# ==>
import itertools
for x in itertools.dropwhile(lambda x:x==2, iterable):
    print(x)
