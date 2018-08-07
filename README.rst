COAT_Geonode
========================

This project was created by using GeoNode project template
https://github.com/GeoNode/geonode-project.

Requirements
------------

In order to run COAT GeoNode you need to have either Docker or Vagrant and VirtualBox installed.

Quick Start
-----------

Vagrant
"""""""

Clone COAT GeoNode code and go to the downloaded directory:

.. code-block::

   $ git clone https://github.com/NINAnor/coat_geonode.git
   $ cd coat_geonode

Bring COAT virtual machine up:

.. code-block::

   $ vagrant up

GeoServer starts automatically. To start GeoNode log in to COAT virtual machine
and go to the synchronized directory. Then start GeoNode.

.. code-block::

   $ vagrant ssh
   $ cd /vagrant/coat_geonode
   $ ./vagrant-provision/start_geonode.sh

GeoServer runs on http://127.0.0.1:8080/geoserver/web/ on your host machine.
For GeoNode it is http://127.0.0.1:8000/.
