s3s
===

Upload System Data to S3

Intro
-----

This tool is designed to help upload EC2 system information to S3 at system shutdown.  A [sosreport](https://github.com/sosreport/sos) is generated and uploaded to S3.  The S3S_BUCKET environment variable sets the S3 bucket name.
