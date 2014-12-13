FROM centos:centos6
MAINTAINER shawn@siefk.as

RUN yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum -y install python-pip python-argparse

RUN yum -y install git
RUN git clone https://github.com/shawnsi/s3s

WORKDIR ./s3s
RUN pip install -r requirements.txt
CMD python s3s.py
