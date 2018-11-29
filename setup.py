from setuptools import setup



setup(
    name='iter_lint',
    version='0.1',
    py_modules=['iter_lint'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        name=script:cli
    ''',
)