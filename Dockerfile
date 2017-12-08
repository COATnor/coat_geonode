FROM ubuntu:16.04

RUN apt-get update && apt-get install -y sudo wget

ADD . /root
RUN chmod +x /root/docker-provision/main.sh
RUN /root/docker-provision/main.sh

# GeoServer port
EXPOSE 8080
# GeoNode port
EXPOSE 8000

# go to /root directory
WORKDIR /root

# start PostgreSQL
ENTRYPOINT /etc/init.d/postgresql start && /bin/bash
