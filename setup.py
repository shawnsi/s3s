#!/usr/bin/env python

from setuptools import setup

setup(
    name='s3s',
    version='0.0.1',
    author='Shawn Siefkas',
    author_email='shawn.siefkas@meredith.com',
    description='Upload System Data to S3',
    install_requires=[
        'boto',
        'docopt',
        'six',
        'sosreport',
    ],
    setup_requires=[
    ],
    test_suite='tests',
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
