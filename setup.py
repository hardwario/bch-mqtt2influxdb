# -*- coding: utf-8 -*-
import setuptools
import os
import re
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='mqtt2influxdb',
    version=find_version('mqtt2influxdb', '__init__.py'),
    description='MQTT to InfluxDB',
    author='HARDWARIO s.r.o.',
    author_email='karel.blavka@hardwario.com',
    url='https://github.com/hardwario/bch-mqtt2influxdb',
    include_package_data=True,
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read('requirements.txt'),
    license='MIT',
    keywords=['mqtt', 'influxdb', 'Hardwatio', 'TOWER', 'BigClown'],
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
    platforms='any',
    entry_points='''
        [console_scripts]
        mqtt2influxdb=mqtt2influxdb.cli:main
    '''
)
