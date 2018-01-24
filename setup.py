# coding=utf-8
import codecs

from setuptools import setup

with codecs.open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
        name='unimatrix',
        url='https://github.com/will8211/unimatrix',
        author='William Mannard',
        description='Python script to simulate the display from "The Matrix" in terminal',
        long_description=readme,
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        py_modules=['unimatrix'],
        entry_points={
            'console_scripts': ['unimatrix=unimatrix:main'],
        }
)
