# Iter Lint
A linting/refactoring library for python iterating best practices

## Use cases

### Range(len(iterable))
```py
for i in range(len(iterable)):
    x = iterable[i]
    do_thing(x,i)
```
will be fixed to 
```py
for x,i in enumerate(iterable):
    do_thing(x,i)
```