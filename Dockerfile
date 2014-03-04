FROM ubuntu:quantal
MAINTAINER Laurens Van Houtven, _@lvh.io

RUN apt-get update # 2014-03-04 14:52
RUN apt-get install -y python-setuptools python-pip git build-essential python-dev libffi-dev
RUN pip install tox

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs ruby-compass

RUN git clone https://github.com/crypto101/website.git /var/website # 2014-03-03 17:22

ADD local/cert-chain.pem /var/website/local

WORKDIR /var/website/static
RUN npm install -g grunt-cli 2>&1
RUN npm install 2>&1 # 2014-03-04 14:52
RUN grunt build

WORKDIR /var/website
RUN tox -e py27

RUN apt-get remove -y python-setuptools python-pip git build-essential python-dev libffi-dev
RUN apt-get remove -y nodejs ruby-compass
RUN apt-get -y autoremove

ENV CERTIFICATE /var/website/local/cert-chain.pem
ENV STATIC_PATH /var/website/static/dist
ENTRYPOINT run
