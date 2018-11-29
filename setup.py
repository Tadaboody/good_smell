from setuptools import setup


from setuptools import setup


setup(
    name='iter_lint',
    version='0.1',
    py_modules=['iter_lint'],
    install_requires=[
        'fire==0.1.3',
        'astor==0.7.1',
        'astpretty==1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'iter_lint=iter_lint:main'
        ]
    }
)
