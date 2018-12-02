from setuptools import setup


import sys
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner==4.2'] if needs_pytest else []

setup(
    name='iter_lint',
    version='0.1',
    py_modules=['iter_lint'],
    install_requires=[
        'fire==0.1.3',
        'astor==0.7.1',
        'astpretty==1.4.0',
    ],
    setup_requires=[] + pytest_runner,
    tests_require=['pytest==4.0.1', 'autopep8==1.4.3'],
    entry_points={
        'console_scripts': [
            'iter_lint=iter_lint:main'
        ]
    }
)
