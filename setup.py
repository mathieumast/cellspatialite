#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cellspatialite',
    version='1.0.0',
    packages=['cellspatialite', 'cellspatialite.test'],
    author='Mathieu',
    description='cellspatialite',
    install_requires= ['pysqlite', 'pandas', 'docopt'],
    license='MIT',
    entry_points = {
        'console_scripts': [
            'cellspatialite = cellspatialite.cellspatialite:main',
        ],
    },

)