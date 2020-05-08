# Good Smell - it makes your code smell good! 
A linting/refactoring library for python best practices and lesser-known tricks  
---
[![Build Status](https://travis-ci.com/Tadaboody/good_smell.svg?branch=master)](https://travis-ci.com/Tadaboody/good_smell) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi version](https://pypip.in/v/good_smell/badge.png)](https://pypi.org/project/good-smell/)
[![codecov](https://codecov.io/gh/Tadaboody/good_smell/branch/master/graph/badge.svg)](https://codecov.io/gh/Tadaboody/good_smell)

---

This Tool tries to find bits of code that are possible to make more pythonic, more beautiful by using the language features and standard library functions you might not know about

For example
Directly nested for loops (nested-for)
```py
for i in seq_a:
    for j in seq_b:
        print(i, j)
```
will be flattened using [itertools.product](https://docs.python.org/3/library/itertools.html#itertools.product)
```py
import itertools
for i, j in itertools.product(seq_a, seq_b):
    print(i, j)
```
For a full list - check the list of [implemented smells](docs/smell_list.md)
## Installing:
```sh
pip install good_smell 
```
## Usage (Is likely to change when version 1.0 is released):
``
good_smell warn - Print warnings about smells in the code
``
```sh
good_smell warn PATH
good_smell warn --path PATH
```
Alternativly you can run it through [flake8](http://flake8.pycqa.org/en/latest/). Smells will be with the code SMLxxx  

``good_smell fix - Print a fixed version of the code``
```sh
good_smell fix PATH [STARTING_LINE] [END_LINE]
good_smell fix --path PATH [--starting-line STARTING_LINE] [--end-line END_LINE]
```

## Developing
See [contributing guide](CONTRIBUTING)
