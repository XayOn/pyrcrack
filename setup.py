#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import pyrcrack


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'psutil'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pyrcrack',
    version=pyrcrack.__version__,
    description="Simple aircrack-ng implementation in python, giving access to common commands and way to read its output / control its execution",
    long_description=readme + '\n\n' + history,
    author="David Francos Cuartero",
    author_email='opensource@davidfrancos.net',
    url='https://github.com/XayOn/pyrcrack',
    packages=[
        'pyrcrack',
    ],
    package_dir={'pyrcrack':
                 'pyrcrack'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pyrcrack',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
