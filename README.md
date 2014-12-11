s3s
===

Upload System Data to S3

Intro
-----

This tool is designed to help upload EC2 system information to S3 at system shutdown.  Currently the /tmp/s3s directory is archived and gzipped then placed in key formatted as *hostname*-*epochtime*.  The S3S_BUCKET environment variable sets the S3 bucket name.
