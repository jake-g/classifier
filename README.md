# Virtual Machine

#### Requires:
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [VirtualBox  Extension Pack](http://download.virtualbox.org/virtualbox/5.0.10/Oracle_VM_VirtualBox_Extension_Pack-5.0.10-104061.vbox-extpack)

#### Vagrant Usage:
* Run `vagrant up` in the root directory of the repo to open the vm
* `vagrant reload`can reload a running vm
*  `vagrant provision` or `vagrant up --provision` will rerun the install scripts found in the `Vagrantfile`
* To stop the vm run `vagrant halt`
* To completely delete the virtual machine use `vagrant destroy`

#### Web App Usage
1. `vagrant up && vagrant ssh` to boot and login to the server. Note the first time will take some time since it has to download the pretrained weights
2. `cd /vagrant` the vagrant folder on the server is equivalent to the root folder on the host machine. Use this to share files between host and server.
3. Run the backend with `python application.py`. This starts the backend on `localhost:5000`. This port is forwarded from the virtual server to the host.
4. On the host machine, open a web browser and navigate to `localhost:5000` and follow the prompt to classify an image
5. The uploaded images get saved in the `uploads/` folder
