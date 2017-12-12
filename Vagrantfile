# coding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Ubuntu 64 bit
  config.vm.box = "xenial64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box"
  config.vm.hostname = "coat"

  # synced folder
  config.vm.synced_folder ".", "/vagrant/coat_geonode"

  config.vm.define "coat" do |server|
    # port forwarding
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.network "forwarded_port", guest: 8000, host: 8000

    # provision script that runs when creating virtual machine
    config.vm.provision :shell, path: "vagrant-provision/main.sh"

    # script that runs always
    # starts GeoServer
	config.vm.provision :shell, path: "vagrant-provision/start_geoserver.sh", run: 'always'

    config.vm.provider "virtualbox" do |vb|
      # RAM
      vb.customize ["modifyvm", :id, "--memory", "2048"]
      # CPU
      vb.customize ["modifyvm", :id, "--cpus", "2"]
    end
  end
end
