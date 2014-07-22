#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [
    'click',
    'textblob',
    'twython',
]

setup(
    name='KareninaClones',
    version='0.1.0',
    description='A library for tweeting Anna Karenina Principle snowclones.',
    author='Daniel D. Beck',
    author_email='me@danieldbeck.com',
    url='https://github.com/ddbeck/KareninaClones',
    packages=[
        'KareninaClones',
    ],
    package_dir={'KareninaClones':
                 'KareninaClones'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    entry_points="""
        [console_scripts]
        kareninaclones=KareninaClones.main:main
    """
)
