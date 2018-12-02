from setuptools import setup


import sys
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner==4.2'] if needs_pytest else []

setup(
    name='good_smell',
    version='0.1',
    py_modules=['good_smell'],
    install_requires=[
        'fire==0.1.3',
        'astor==0.7.1',
        'astpretty==1.4.0',
    ],
    setup_requires=[] + pytest_runner,
    tests_require=['pytest==4.0.1',
                   'mccabe==0.6.1', 'pytest-mccabe==0.1',
                   'autopep8==1.4.3'],
    entry_points={
        'console_scripts': [
            'good_smell=good_smell:main'
        ]
    }
)
