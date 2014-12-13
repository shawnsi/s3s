#!/usr/bin/env python
"""s3s

Usage:
    s3s upload <bucket>
    s3s hook <queue> <bucket>

Options:
    -h --help   Show this screen.
    --version   Show version.
"""
from __future__ import print_function

import json
import os
import time

import boto
import boto.s3.key
import boto.sqs

from docopt import docopt
from sos.sosreport import SoSReport

def get_instance_id():
    return boto.utils.get_instance_metadata()['instance-id']

def get_key(bucket):
    c = boto.connect_s3()
    b = c.create_bucket(bucket)
    return boto.s3.key.Key(b)

def get_queue(queue):
    c = boto.sqs.connect_to_region(get_region())
    q = c.get_queue(queue)
    q.set_message_class(boto.sqs.message.RawMessage)
    return q

def get_region():
    return boto.utils.get_instance_identity()['document']['region']

def is_local_termination(message):
    payload = json.loads(message.get_body())

    if payload['EC2InstanceId'] == get_instance_id():
        if payload['LifecycleTransition'] == 'autoscaling:EC2_INSTANCE_TERMINATING':
            return True

def upload(bucket):
    # Grab an S3 key before running sosreport
    key = get_key(bucket)

    # Run sosreport in batch mode
    sos = SoSReport(['--batch'])
    sos.execute()

    # Set the key name to the sosreport archive name
    archive = sos.archive.name()
    key.key = os.path.split(archive)[-1]

    # Upload the sosreport archive to S3
    key.set_contents_from_filename(archive)

if __name__ == '__main__':
    args = docopt(__doc__, version='s3s 0.0.1')

    bucket = args['<bucket>']

    if args['hook']:
        queue = get_queue(args['<queue>'])

        while True:
            for message in queue.get_messages():
                if is_local_termination(message):
                    upload(bucket)
                    queue.delete_message(message)

            time.sleep(1)

    if args['upload']:
        upload(bucket)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
