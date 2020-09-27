# Contributing
:tada:Thank you so much for taking the time to contribute:tada:
## Wait!
Before trying to help please tell us what's wrong.
Please check if there is an [open issue](https://github.com/Tadaboody/good_smell/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) with your problem.
If there isn't one, [create one](https://github.com/Tadaboody/good_smell/issues/new/choose)

If you want to contribute code you will need to:

## Create an enviroment
This project uses [Poetry](https://python-poetry.org/docs) for package managment

Clone the repository and run inside it:
```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python # Install poetry on your machine
poetry install # Create a new enviroment and install the development requirements
poetry shell # Activate 
run pre-commit install # Install pre-commit hooks
```
## Write the solution
New smells are implented in a new file in `good_smell/smells`, by creating a class that inherits `good_smell/lint_smell.py`.
After implementing the methods add the class to the list `implemented_smells` in `good_smell/smells/__init__.py`

If you're new to parsing and transforming ASTs, [green tree snakes](https://greentreesnakes.readthedocs.io/en/latest/index.html) is a great guide to the basics.
## Write the tests
Inside the relevant file in the `tests/examples` dir (Or a new), the tests are formatted like this
```py
#:<Test description>
#<Comma-seperated list of warning symbols emmited> or "None"
<Python code emitting the smells>
# ==>
<Python code after fixing the smell>
# END
```
See [the example file](tests/examples/example.py) for an example
## Run the tests
Activate your virtual enviroment and run
```sh
pytest
```
To run a specific test run 
```sh
pytest -k <Test description>
```
