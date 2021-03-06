#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'flask',
    'ldap3',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='flask_open_directory',
    version='0.1.1',
    description="MacOS OpenDirectory Authorization Middleware for Flask",
    long_description=readme + '\n\n' + history,
    author="Michael Housh",
    author_email='mhoush@houshhomeenergy.com',
    url='https://github.com/m-housh/flask_open_directory',
    packages=[
        'flask_open_directory',
    ],
    package_dir={'flask_open_directory':
                 'flask_open_directory'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='flask_open_directory',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: MacOS X',
        'Framework :: Flask',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
