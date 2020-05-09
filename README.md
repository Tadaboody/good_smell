# Good Smell - it makes your code smell good! 
A linting/refactoring library for python best practices and lesser-known tricks  
---
![Build](https://github.com/tadaboody/good_smell/workflows/Python%20package/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi version](https://pypip.in/v/good_smell/badge.png)](https://pypi.org/project/good-smell/)

---

This Tool tries to find bits of code that are possible to make more pythonic, more beautiful by using the language features and standard library functions you might not know about

For example
Directly nested for loops (nested-for)
```py
for i in seq_a:
    for j in seq_b:
        print(i, j)
```
will be flattened to a nested comprehension
```py
import itertools
for i, j in ((i,j) for i in seq_a for j in seq_b):
    print(i, j)
```
For a full list - check the list of [implemented smells](docs/smell_list.md)
## Installing:
```sh
pip install good_smell 
```
## Usage (Is likely to change when version 1.0 is released):

To issue warnings, good_smell installs itself as a [flake8](http://flake8.pycqa.org/en/latest/) plugin with error codes starting with SML.

To automatically fix the code use ``good_smell fix``:

```sh
good_smell fix PATH >PATH
good_smell fix PATH [--starting-line STARTING_LINE] [--end-line END_LINE]
```

## Developing
See [contributing guide](CONTRIBUTING)
