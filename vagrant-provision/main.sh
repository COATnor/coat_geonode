#! /usr/bin/env bash

sudo apt-get update;
sudo apt-get install -y python-pip git;
pip install --upgrade pip;

cd /vagrant/coat_geonode;
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

# install PostgreSQL
sudo apt-get update;
sudo apt-get install -y \
    postgresql             \
    postgis                \
    postgresql-9.5-postgis-scripts \
    postgresql-contrib;

# create user
sudo -u postgres psql -c "CREATE USER geonode WITH PASSWORD 'geonode'"
# create databases
sudo -u postgres createdb -O geonode geonode
sudo -u postgres createdb -O geonode geonode_data
sudo -u postgres psql -d geonode_data -c 'CREATE EXTENSION postgis;'
sudo -u postgres psql -d geonode_data -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
sudo -u postgres psql -d geonode_data -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'

# replace a line in the pg_hba.conf file for PostgreSQL
sudo sh -c "sed -e 's/local   all             all                                     peer/local   all             all                                     trust/' < /etc/postgresql/9.5/main/pg_hba.conf > /etc/postgresql/9.5/main/pg_hba.conf.tmp";
sudo mv /etc/postgresql/9.5/main/pg_hba.conf.tmp /etc/postgresql/9.5/main/pg_hba.conf;
sudo service postgresql restart;

# migrate COAT
cd /vagrant/coat_geonode;
python manage.py migrate;



