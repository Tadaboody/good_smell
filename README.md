# Good Smell - it makes your code smell good! 
A linting/refactoring library for python best practices and lesser-known tricks  
---
[![Build Status](https://travis-ci.com/Tadaboody/good_smell.svg?branch=master)](https://travis-ci.com/Tadaboody/good_smell) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi version](https://pypip.in/v/good_smell/badge.png)](https://pypi.org/project/good-smell/)
---

## Installing:
```sh
pip install good_smell 
```
## Usage:
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
## Supported code smells:

``Range(len(sequence))``
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
``Directly nested for loops``
```py
for i in seq_a:
    for j in seq_b:
        print(i, j)
```
to
```py
import itertools
for i, j in itertools.product(seq_a, seq_b):
    print(i, j)
```

## Developing
Clone the repository and run inside it
```sh
pip install -e .[dev]
```
This will install the requirements and the package itself, updating when you edit the code.

Tests are run using pytest, simply run:
```sh
pytest
```