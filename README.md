# Iter Lint [![Build Status](https://travis-ci.com/Tadaboody/iter_lint.svg?branch=master)](https://travis-ci.com/Tadaboody/iter_lint)
A linting/refactoring library for python iterating best practices

## Installing:
```sh
python setup.py install
```
## Usage:
```sh
Usage:       iter_lint PATH [STARTING_LINE] [END_LINE]
             iter_lint --path PATH [--starting-line STARTING_LINE] [--end-line END_LINE]
```
## Supported code smells:

### Range(len(sequence))
```py
for i in range(len(sequence)):
    x = sequence[i]
    do_thing(x,i)
```
will be fixed to 
```py
for i, x in enumerate(sequence):
    do_thing(x,i)
```
### Directly nested for loops
```py
for i in seq_a:
    for j in seq_b:
```
to
```py
import itertools
for i, j in itertools.product(seq_a, seq_b):
    print(i, j)
```