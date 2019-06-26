#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import (
    setup,
    find_packages,
)


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


install_requires = [
    'pytest-play>=2.0',
    'pytest>=3.0.7',
    'pytest-variables[yaml]',
    'pytest-pypom-navigation',
    'pytest-splinter',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'mock',
    'zope.interface',
]

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme',
    ]

setup(
    name='play_selenium',
    version='0.0.3',
    author='Davide Moro',
    author_email='davide.moro@gmail.com',
    maintainer='Davide Moro',
    maintainer_email='davide.moro@gmail.com',
    license='Apache Software License 2.0',
    url='https://github.com/davidemoro/play_selenium',
    description='pytest plugin that let you drive a '
                'browser with Selenium',
    long_description=open("README.rst").read() + "\n" +
    open("CHANGES.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'playcommands': [
            'selenium = play_selenium.providers:SplinterCommandProvider',
        ],
    },
    extras_require={
        'tests': tests_require,
        'docs': docs_require,
    },
)
