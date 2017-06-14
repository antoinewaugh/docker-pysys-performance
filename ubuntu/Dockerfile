FROM ubuntu:14.04

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  apt-get install -y wget && \
  rm -rf /var/lib/apt/lists/*

# Insatll Pysys.

RUN \
  wget https://downloads.sourceforge.net/project/pysys/pysys/1.2.0/PySys-1.2.0.tar.gz && \
  tar -xvf PySys-1.2.0.tar.gz && \
  cd Pysys-1.2.0 && \
  python setup.py install


COPY . /test


