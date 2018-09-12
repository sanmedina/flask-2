#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from setuptools import find_packages
from setuptools import setup

setup(
    name='my_app',
    version='1.0.0',
    license='GNU General Public License V3',
    author='Dev Medina',
    author_email='devsanmedina@protonmail.com',
    description='Hello world app for Flask',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-wtf',
        'flask-login',
        'requests',
        'flask-openid',
    ],
    extras_require={
        'dev': [
            'pylint',
            'autopep8',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
