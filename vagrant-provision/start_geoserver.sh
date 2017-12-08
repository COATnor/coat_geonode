#! /usr/bin/env bash

cd /vagrant/coat_geonode/geonode;
nohup sudo paver start_geoserver &

sleep 30;
