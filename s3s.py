#!/usr/bin/env python

from __future__ import print_function

import os

import boto
from sos.sosreport import SoSReport

s3 = boto.connect_s3()

def get_bucket():
    return s3.create_bucket(os.environ['S3S_BUCKET'])

def get_key():
    return boto.s3.key.Key(get_bucket())

if __name__ == '__main__':
    # Grab an S3 key before running sosreport
    key = get_key()

    # Run sosreport in batch mode
    sos = SoSReport(['--batch'])
    sos.execute()

    # Set the key name to the sosreport archive name
    archive = sos.archive.name()
    key.key = os.path.split(archive)[-1]

    # Upload the sosreport archive to S3
    key.set_contents_from_filename(archive)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
