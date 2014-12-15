s3s
===

[![Build Status](https://travis-ci.org/shawnsi/s3s.png)](https://travis-ci.org/shawnsi/s3s)

Upload System Data to S3

Intro
-----

This tool is designed to help upload EC2 system information to S3 at system shutdown.  A [sosreport](https://github.com/sosreport/sos) is generated and uploaded to S3.

This is particularly useful when an EC2 autoscaling action terminates an instance due to a failed health check.  The data collected can help perform root cause analysis on the terminated instance.

AWS Credentials
---------------

Currently your AWS credentials must be set as [environment variables](http://boto.readthedocs.org/en/latest/boto_config_tut.html) for boto to parse.  [IAM roles for EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) can be used to seamlessly grant access to AWS resources.

Upload to S3
------------

A sosreport can be uploaded to S3 like so:

```bash
$ s3s upload <bucket>
```

This could be called at system termination via the init system but that is currently left as an exercise for the reader.

ASG Lifecycle Hook
------------------

An [Auto Scaling Group Lifecycle Hook](http://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/AutoScalingGroupLifecycle.html) can be used to notify s3s of pending instance termination.  S3s will monitor the provided SQS queue for a [Terminating:Wait](http://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/AutoScalingGroupLifecycle.html) message that corresponds to the local EC2 instance.  When the message is received s3s will perfom an upload to the provided S3 bucket.

```bash
$ s3s hook <queue> <bucket>
```
