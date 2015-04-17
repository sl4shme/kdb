#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages

PROJECT = 'kdb'
VERSION = '0.0.1'


try:
    # long_description = open('README.rst', 'rt').read()
    long_description = 'KDB (Knowledge DataBase) is a lightweight simple \
    solution to store, retrieve and manage knowledges. \
    If one day you said to yourself: "I need to write this command somewhere" \
    or "This configuration file could be usefull someday". \
    Then KDB is for you. '
except IOError:
    long_description = ''

setup(
    name='KDB',
    version='0.0.1',

    description='KDB (Knowledge DataBase)',
    long_description=long_description,

    author='Pierre-Arthur MATHIEU',
    author_email='pi3rra@root.gg',

    url='https://github.com/sl4shme/kdb',
    download_url='https://github.com/sl4shme/kdb',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Developers',
                 'Intended Audience :: System Administrators',
                 'Environment :: Console',
                 ],

    platforms=['POSIX'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'tinydictdb'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'kdbshell = kdb.shell:main'
        ],
        'kdb.shell': [
            'list = kdb.commands:List',
            'new = kdb.commands:New',
            'delete = kdb.commands:Delete',
            'search = kdb.commands:Search',
        ],
    },

    zip_safe=False,
)
