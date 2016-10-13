FROM ubuntu:14.04

COPY .iot /root/.iot

RUN apt-get update
RUN apt-get install -y python python-serial

RUN apt-get install -y curl socat
RUN curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -
RUN apt-get install -y nodejs
RUN npm install --prefix /root/.iot/node/ socket.io
RUN npm install --prefix /root/.iot/node/ async



