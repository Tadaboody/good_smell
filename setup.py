import sys
from pathlib import Path

from setuptools import setup, find_packages

long_description = Path("README.md").read_text()

setup(
    name="good_smell",
    version="0.13.0",
    packages=find_packages(exclude=("tests",)),
    install_requires=["fire", "astor", "flake8 >= 3.0.0"],
    author="Tomer Keren",
    author_email="tomer.keren.dev@gmail.com",
    description="A linter/refactoring tool to make your code smell better!",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    entry_points={
        "console_scripts": ["good_smell=good_smell:main"],
        "flake8.extension": "SML=good_smell:GoodSmellFlake8",
    },
)
