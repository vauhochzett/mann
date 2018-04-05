""" mann setup """

from setuptools import setup

setup(
    name='mann',
    version='0.6.1',
    py_modules=['mann'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mann=mann:mann
    ''',
)
