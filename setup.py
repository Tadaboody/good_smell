from setuptools import setup


import sys

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner==4.2"] if needs_pytest else []
dataclasses = (
    ["dataclasses==0.6"] if sys.version_info < (3, 7) else []
)  # Backport of dataclasses from py3.7

setup(
    name="good_smell",
    version="0.1",
    py_modules=["good_smell"],
    install_requires=["fire==0.1.3", "astor==0.7.1", "astpretty==1.4.0"] + dataclasses,
    setup_requires=[] + pytest_runner,
    tests_require=[
        "pytest==4.0.1",
        "mccabe==0.6.1",
        "pytest-mccabe==0.1",
        "autopep8==1.4.3",
    ],
    entry_points={"console_scripts": ["good_smell=good_smell:main"]},
)
