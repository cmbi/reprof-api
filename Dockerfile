FROM python:3.11

# dependencies
RUN apt-get update ; apt-get install -y reprof

# hope
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

# settings
EXPOSE 5001
