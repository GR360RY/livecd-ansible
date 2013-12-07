# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "centos64-x64"
  config.vm.box_url = "https://github.com/2creatives/vagrant-centos/releases/download/v0.1.0/centos64-x86_64-20131030.box"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "livecd-builder.yml"
    ansible.tags = "host_setup_livecd"
    ansible.sudo = true
  end
end
