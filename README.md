# Good Smell - it makes your code smell good! [![Build Status](https://travis-ci.com/Tadaboody/good_smell.svg?branch=master)](https://travis-ci.com/Tadaboody/good_smell)
A linting/refactoring library for python best practices and lesser-known tricks

## Installing:
```sh
python setup.py install
```
## Usage:
```sh
Usage:       good_smell PATH [STARTING_LINE] [END_LINE]
             good_smell --path PATH [--starting-line STARTING_LINE] [--end-line END_LINE]
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

### Running tests
```sh
python setup.py test
```