#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = ['PyYAML>=3.11', 'paho-mqtt>=1.0', 'influxdb', 'schema>=0.6.7', 'jsonpath-ng>=1.4.3', 'pycron>=3.0.0', 'py_expression_eval>=0.3.9']

setup(
    name='mqtt2influxdb',
    packages=["mqtt2influxdb"],
    version='@@VERSION@@',
    description='MQTT to InfluxDB',
    author='HARDWARIO s.r.o.',
    author_email='karel.blavka@bigclown.com',
    url='https://github.com/bigclownlabs/bch-mqtt2influxdb',
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords=['BigClown', 'mqtt', 'influxdb'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Environment :: Console'
    ],
    entry_points='''
        [console_scripts]
        mqtt2influxdb=mqtt2influxdb.cli:main
    ''',
    long_description='''
BigClown tool for storage data from MQTT to InfluxDB
'''
)
