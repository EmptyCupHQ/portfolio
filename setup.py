from setuptools import setup

setup(
    name='portfolio',
    version='0.0.1',
    py_modules=['portfolio'],
    install_requires=[
        'mkdocs-material',
        'flask'
    ],
    entry_points={
        'console_scripts': [
            'po = src.cli.cli:admin',
        ],
    },
)
