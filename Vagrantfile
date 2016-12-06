# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "puppetlabs/ubuntu-14.04-64-nocm"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
 
 	#config.ssh.insert_key = false
	#config.vm.provision "file",  source: "pubkey", destination: "/home/vagrant/.ssh/pubkey.pub"
  #config.vm.provision "shell", inline: "cat /home/vagrant/.ssh/pubkey.pub >> /home/vagrant/.ssh/authorized_keys"
	#config.ssh.public_key_path = "pubkey"
	#config.ssh.private_key_path = "privkey"

 	['1','2'].each do |number|
    config.vm.define "vm#{number}" do |vm|
      vm.vm.network "private_network", ip: "10.0.0.20#{number}"
      vm.vm.synced_folder "website", "/app"

    end
end

config.vm.define "lb1" do |lb|
    lb.vm.network "private_network", ip: "10.0.0.10"
    lb.vm.network "forwarded_port", guest: 80, host: 8080
    lb.vm.provision "shell", inline: <<-SHELL
     export DEBIAN_FRONTEND=noninteractive
     apt-get update -qq
     apt-get install python-dev python-pip build-essential libssl-dev libffi-dev -qq -y --no-install-recommends
		 #latest 2.1.3 branch...
		 pip install ansible==2.1.3
   SHELL
  lb.vm.synced_folder "ansible", "/ansible"

   lb.vm.provision :ansible_local do |ansible|
      ansible.playbook       = "/ansible/playbook.yml"
      ansible.verbose        = 'v'
#      ansible.install        = true
      ansible.limit          = "all" # or only "nodes" group, etc.
      ansible.inventory_path = "inventory"
      ansible.sudo           = true
    end
end


end
