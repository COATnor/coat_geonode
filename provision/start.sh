#! /usr/bin/env bash

cd /vagrant/geonode;
nohup sudo paver start_geoserver &

sleep 30;

# cd /vagrant/coat_geonode;
# python manage.py runserver 0.0.0.0:8000;
