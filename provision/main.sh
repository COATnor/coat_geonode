#! /usr/bin/env bash

sudo apt-get update;
sudo apt-get install -y python-pip git;

cd /home/ubuntu;
git clone https://github.com/NINAnor/coat_geonode.git;
git clone -b 2.6.x https://github.com/GeoNode/geonode.git;
# install manually because pip can not install binary dependencies
sudo apt-get install python-shapely -y;
sudo pip install -e geonode && sudo pip install -r geonode/requirements.txt;

# install specific version of Shapely - this might change in the future
sudo pip install --upgrade Shapely==1.5.17;

cd geonode && paver setup;

# install manually because pip can not install binary dependencies;
sudo apt-get install -y python-gdal;

python manage.py migrate;

# create user 'admin'
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'nimda')" | python manage.py shell
python manage.py loaddata geonode/base/fixtures/initial_data.json;
python manage.py loaddata geonode/base/fixtures/default_oauth_apps.json;

# install Java 8
cd /tmp;
wget --quiet --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe78cdb6d0/jdk-8u152-linux-x64.tar.gz -O jdk.tar.gz;
mkdir /opt/jdk;
tar -zxf jdk.tar.gz -C /opt/jdk;
update-alternatives --install /usr/bin/java java /opt/jdk/jdk1.8.0_152/bin/java 100;
update-alternatives --install /usr/bin/javac javac /opt/jdk/jdk1.8.0_152/bin/javac 100;
