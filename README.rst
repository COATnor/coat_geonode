COAT_Geonode
========================

This project was created by using GeoNode project template
https://github.com/GeoNode/geonode-project.

Requirements
------------

In order to run COAT GeoNode you need to have Vagrant and VirtualBox installed.

Quick Start
-----------

You can choose Vagrant or Docker.

Vagrant
"""""""

Clone COAT GeoNode code and go to the downloaded directory:

.. code-block::

   git clone https://github.com/NINAnor/coat_geonode.git
   cd coat_geonode

Bring COAT virtual machine up:

.. code-block::

   vagrant up

GeoServer starts automatically. To start GeoNode log in to COAT virtual machine
and go to the synchronized directory. Then start GeoNode.

.. code-block::

   vagrant ssh
   cd /vagrant/coat_geonode
   ./vagrant-provision/start_geonode.sh

GeoServer runs on http://127.0.0.1:8080/geoserver/web/ on your host machine.
For GeoNode it is http://127.0.0.1:8000/.

Docker
""""""

Clone COAT GeoNode code and go to the downloaded directory:

.. code-block::

   git clone https://github.com/NINAnor/coat_geonode.git
   cd coat_geonode

Download COAT Docker image and clone GeoNode code to your host:

.. code-block::

   docker pull ninanor/coat_geonode
   git clone -b 2.6.x https://github.com/GeoNode/geonode.git

Then create a container with forwarded ports and run it in interactive mode:

.. code-block::

   docker run -it -v $(pwd):/root -p 8000:8000 -p 8080:8080 --name coat ninanor/coat_geonode

When you are "in the container" setup Paver. This step is required to do
only once.

.. code-block::

   cd geonode && paver setup && cd ..

Finally you can start GeoServer and GeoNode:

.. code-block::

   ./docker-provision/start_geoserver.sh
   ./docker-provision/start_geonode.sh

GeoServer runs on http://127.0.0.1:8080/geoserver/web/ on your host machine.
For GeoNode it is http://127.0.0.1:8000/.

After you exit container you can log in again by the following command:

.. code-block::

   docker start -a -i coat
