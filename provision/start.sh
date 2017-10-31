#! /usr/bin/env bash

cd /home/ubuntu/geonode;
nohup sudo paver start_geoserver &

sleep 40;

python manage.py runserver 0.0.0.0:8000;
