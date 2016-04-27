# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
    v.name = "woof"
    v.memory = 1024
    v.cpus = 2

  # forward port guest machine:5000 -> host machine:5000
  # port 5000 is default for flask web app
  config.vm.network "forwarded_port", guest: 5000, host: 5000
end

# Bash Script
config.vm.provision "shell", inline: <<-SHELL
  sudo apt-get update

  # install programs
  echo "---------------INSTALLING PACKAGES---------------"
  declare -a program=(
    "curl" "git" "npm" "vim" "htop"
    "python" "python-setuptools" "python-pip" "python-numpy"
    "build-essential" "gcc" "g++"
    "gfortran" "libopenblas-base" "libgfortran3" "cmake"
    "imagemagick"
   )
  for i in "${program[@]}"
    do
       echo "Installing $i ..."
       apt-get -y install "$i"
    done

  # install pip python packages
  echo "---------------INSTALLING PYTHON PACKAGES---------------"
  declare -a py=(
      "flask"
      "virtualenv"
      "requests"
      )

  for i in "${py[@]}"
    do
       echo "Installing $i ..."
       pip install "$i"
    done

  echo 'Copying terminal settings...'
  cp /vagrant/classifier/.bashrc /home/vagrant
  
  # Get pretrained weights
  python /vagrant/classifier/download_weights.py
  
  # upgrade and clean up
  sudo apt-get upgrade -y
  sudo apt-get autoremove -y
  sudo apt-get autoclean -y
SHELL
end
