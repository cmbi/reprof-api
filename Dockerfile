FROM python:2.7-onbuild

RUN apt-get update ; apt-get install -y reprof

WORKDIR /usr/src/app
EXPOSE 5001
