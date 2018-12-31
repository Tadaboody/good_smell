import sys
from pathlib import Path

from setuptools import setup, find_packages

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner==4.2"] if needs_pytest else []
long_description = Path("README.md").read_text()

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner==4.2"] if needs_pytest else []
dataclasses = (
    [] if sys.version_info < (3, 7) else []
)  # Backport of dataclasses from py3.7

tests_require = [
    "pytest==4.0.1",
    "mccabe==0.6.1",
    "pytest-mccabe==0.1",
    "autopep8==1.4.3",
    "pytest-cov==2.6.0",
]
setup(
    name="good_smell",
    version="0.11.0",
    packages=find_packages(exclude=("tests",)),
    setup_requires=[] + pytest_runner,
    install_requires=[
        "fire==0.1.3",
        "astor==0.7.1",
        "astpretty==1.4.0",
        "flake8 >= 3.0.0",
        'dataclasses==0.6;python_version<"3.7"',
    ],
    author="Tomer Keren",
    author_email="tomer.keren.dev@gmail.com",
    description="A linter/refactoring tool to make your code smell better!",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Framework :: Flake8",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    url="https://github.com/Tadaboody/good_smell",
    tests_require=tests_require,
    entry_points={
        "console_scripts": ["good_smell=good_smell:main"],
        "flake8.extension": "SML=good_smell:GoodSmellFlake8",
    },
    extras_require={"dev": tests_require},
)
