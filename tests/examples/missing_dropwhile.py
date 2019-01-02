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
