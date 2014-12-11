#!/usr/bin/env python

from __future__ import print_function

import os
import socket
import tarfile
import tempfile
import time

import boto

def get_key():
    c = boto.connect_s3()
    bucket = c.create_bucket(os.environ['S3S_BUCKET'])
    key = boto.s3.key.Key(bucket)
    hostname = socket.gethostname()
    timestamp = str(int(time.time()))
    key.key = '%s-%s.tar.gz' % (hostname, timestamp)
    return key

def get_archive():
    temp = tempfile.mktemp()
    tar = tarfile.open(temp, 'w:gz')
    tar.add('/tmp/s3s')
    tar.close()
    return temp

if __name__ == '__main__':
    key = get_key()
    key.set_contents_from_filename(get_archive())


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
