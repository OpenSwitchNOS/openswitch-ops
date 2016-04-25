ANSIBLE
----------------

##Contents
   - [Overview](#overview)
   - [Prerequisites](#prerequisites)
   - [Ansible Installation](#ansible-installation)
      - [Setting up basic configuration on control machine](#setting-up-basic-configuration-on-control-machine)
          - [Default configuration for Ansible](#default-configuration-for-ansible)
	  - [Declaring inventory/hosts file](#declaring-inventory/hosts-file)
          - [Verifying Ansible installation](#verifying-ansible-installation)
   - [Playbooks](#playbooks)
   - [Roles](#roles)
     - [Ansible galaxy](#ansible-galaxy)
   - [Communicating with the Openswitch](#communicating-with-the-openswitch)
      - [ssh communication](#ssh-communiation)

### Overview
This guide provides details about installing Ansible, basics of Ansible and communicating with the Openswitch using Ansible playbooks and modules. Ansible is an IT automation tool which is lightweight and has following important characteristics:

- Ansible doesn’t need a master server you only need a control machine to run the playbooks and roles on the hosts.
- No need to install anything on the hosts.
- Ansible works via SSH so SSH keys are our friends.
- We only need IP reach-ability to the servers and we run the scripts/playbooks.
- Managing automation code is writing yaml files which is equivalent to writing human readable ordered commands.

### Prerequisites
The basic requirement to use Ansible is to have a Linux/BSD/mac/centos OS based control machine in the infrastructure. Windows machine can not be used as a control machine right now.
For the installation, it is recommended on the Ansible website to use 'pip' which is the python package manager to install Ansible.

### Installing Ansible

As per the flavor of the operating system, there are different ways to install Ansible.

```
Recommended by Ansible official documentation for linux:

$sudo pip install Ansible

on mac OS:

$brew install Ansible

on centos OS:

$yum install Ansible

Ansible can also be installed using apt-get provided all the package requirements are taken care of:

$sudo apt-get install Ansible
```

For more information and explanation about installing Ansible on your flavor of OS please refer to,

http://docs.ansible.com/ansible/intro_installation.html#getting-ansible

A working Ansible control machine docker image is uploaded on the docker hub and is being used for running the tests.
The command to pull the Ansible control machine is,
```
docker pull openswitch/ansiblecm
```

####Setting up basic configuration on control machine

#####Default configuration for Ansible
Settings in Ansible can be adjusted via Ansible.cfg. If you use pip install for Ansible, Ansible.cfg is by default present at /etc/Ansible/ location. Changes can be made by creating Ansible.cfg file either in the home directory or in the current directory.
For more information about Ansible Config file, please refer to,

http://docs.ansible.com/ansible/intro_configuration.html


#####Declaring inventory/hosts file

Managing the list of servers or hosts that need to be automated is achieved by crating  an inventory file. inventory file is by default present at /etc/ansible/hosts lcoation. The location of the inventory file can be changed by providing specific location in he ansible.cfg file. Similar to the configuration file, inventory file can also be created in the current directory or home directory to overwrite the default file under /etc/ansible/hosts.

For more information about managing the inventory and options associated with the inventory, please refer to,

http://docs.ansible.com/ansible/intro_inventory.html

Sample inventory:

```
[OpenSwitch]
ops ansible_host=192.168.1.10 ansible_port=22

```

#####Verifying the Ansible installation

To make sure Ansible is properly installed and all requirements are met, we can make use of Ansible modules on the localhost.
For example,
```
$ ansible localhost -m ping
$ ansible localhost -m setup
```

###Playbooks

Playbook are used to automate, configure and orchestrate the infrastructure. As the official documentation explains, playbooks are the design plans and modules are the tools. Playbooks contain plays and plays contain tasks.

Sample playbook with a single play:

```
---
- hosts: OpenSwitch    =======> the hosts to run the playbook on
  remote_user: root    =======> User that will be logged in with
  tasks:
    - name: ping the OpenSwitch  ===> Name/Caption for the task
      ping:                      ===> Ansible module to be used
```

To run the playbook we can use the command below.
```
$ansible-playbook ping.yml
```

To get more insight on writing playbboks, please refer to,

http://docs.ansible.com/ansible/playbooks_intro.html


###Roles

Now that we have an insight about playbooks, for a larger and diverse architecture, the best way to manage the orchesteration is to create and use roles.
Role is an easy way to share the variables, default configuration and host specific configuration in a structured file which is familiar to Ansible.
Role saves the duplication of playbooks and variables.

A typical structure of a role is shown below.

```
site.yml
roles/
   switch/
     files/
     templates/
     tasks/
     handlers/
     vars/
     defaults/
     meta/
```

This role can be executed on the host by running the site.yml file which is shown below.

```
---
- hosts: OpenSwitch
     roles:
     - switch
```

For more detailed explanation about writing roles please refer to,

http://docs.ansible.com/ansible/playbooks_roles.html


####Ansible-galaxy

Ansible-galaxy is not only a website to manage the Ansible roles but also is a command line tool to create and manage the roles.
Following command can be used to create a role using Ansible-galaxy command.
```
$ ansible-galaxy init switch
```
Note: switch is an example role name.

Please go through the following link to get more information about Ansible-galaxy.

http://docs.ansible.com/ansible/galaxy.html


###Communicating with the OpenSwitch

To communicate with the host, we need to have an IP reachability. If we can ping the server and initiate the SSH communication, we can automate the configuration on the host. Communicating with Openswitch is same as well. Ansible connects to the host in our case, OpenSwitch and pushes small programs called Ansible modules. Communication, deployment and automation with OpenSwitch can be  achieved by using three Ansible modules which are specifically developed for OpenSwitch. Please find more information about these modules in the respective links provided beneath each module.

- ops_template : Push configuration to OpenSwitch

https://docs.ansible.com/ansible/ops_template_module.html

- ops_command: Run arbitrary commands on OpenSwitch devices

https://docs.ansible.com/ansible/ops_command_module.html

 - ops_config: Manage OpenSwitch configuration using CLI

https://docs.ansible.com/ansible/ops_config_module.html


These modules are used in the plabooks to be run on the OpenSwitch. After execution of the modules, they are removed by Ansible. No packages or applications are installed on the OpenSwitch.

####ssh communication with the OpenSwitch

We can communicate using passwords but SSH keys with SSH-agents are one of the best ways to communicate. Ansible's "authorized_keys" module can be used to copy the public key from Ansible control machine to the OpenSwitch.

An example playbooks written for the initial communication with the OpenSwitch can be referred from,

http://git.OpenSwitch.net/cgit/OpenSwitch/ops-ansible/tree/examples/utility

Working of the test can be confirmed by following the following commands,
```
$ git clone https://git.OpenSwitch.net/OpenSwitch/ops-build  ops-sim
$ cd ops-sim
$ make configure genericx86-64
$ make devenv_init
$ make devenv_add ops-ansible
$ make testenv_init
$ make testenv_run component ops-ansible

```
####Reference
- http://www.ansible.com
- http://docs.ansible.com
