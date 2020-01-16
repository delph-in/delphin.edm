#!/usr/bin/env python3

import os
from setuptools import setup

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='delphin.edm',
    version='0.1.0',
    description=('Elementary Dependency Match (EDM) is a metric for comparing '
                 'alternate semantic graphs for the same source sentence'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/delph-in/delphin.edm',
    author='Michael Wayne Goodman',
    author_email='goodman.m.w@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    keywords='semantics evaluation delph-in nlp',
    packages=[
        'delphin',
        'delphin.cli',
    ],
    install_requires=[
        'pydelphin >= 1.2.0',
    ],
)
