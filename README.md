
Preface
-------

LiveCDs can be a big help when you need to do a task that cannot be executed from within OS for some reason.
Resizing partitions, changing passwords and firmware updates - is just the beginning of the list.
It is especially welcome when your machine cannot boot from network ( PXE ).

There are lot of very good options like Knoppix, Parted Magic or LiveCDs of popular distributions.
But there are cases when you need custom LiveCD with your scripts, packages and preinstalled software.
Ability to modify root partition using writable snapshot on livecd, allows you to add software and modify configuration
on the fly.
<!-- more -->

LiveCD can be easily flashed to usb or converted to pxe images. Hence, there are plenty of ways to get into your custom livecd.
Booting LiveCD from network can be a great way to bootstrap your hardware before os installation. 

The standard procedure of LiveCD creation requires livecd-tools package together with kickstart file that defines packages list 
and post installation instructions. All postinstall is done using shell scripts which is far from ideal. Tools like Ansible 
are better suitable for doing exactly that. Defining system state with DSL language is much cleaner and easily maintanable.

In the next guide I will show how to create your own custom Centos 6.4 LiveCD using step by step instructions.

Installing Requirements
-----------------------

1. CentOS 6.X machine.
2. livecd-tools, git, python-argparse and ansible - all packages available in EPEL repository.

Install EPEL repository if not already installed:
    yum -y install http://ftp.nluug.nl/pub/os/Linux/distr/fedora-epel/6/i386/epel-release-6-8.noarch.rpm
Install required packages:
    yum -y install livecd-tools git ansible python-argparse
Clone livecd-ansible repository:
    git clone https://github.com/GR360RY/livecd-ansible.git

Building LiveCD the old way
---------------------------

Let start from getting basic livecd configuration kickstart file for CentOS created by Fabian Arrotin (arrfab):
    wget http://people.centos.org/arrfab/CentOS6/LiveCD-DVD/centos6-liveCD-desktop.cfg

`livecd-creator` tool from livecd-tools package is used to create custom livecd.

The example follows:
    livecd-creator -c centos6-liveCD-desktop.cfg -f centos6-desktop

This will create `centos6-desktop.iso` as defined in centos6-liveCD-desktop.cfg.
The file has standard kickstart format and contains two main parts:

#### Services configuration and packages selection:

This part is straightforward. Language, Keyboard and Services are self explanatory.
The same goes for package list - contains yum groups and individual packages.
{% codeblock centos6-liveCD-desktop.cfg lang:bash %}

lang en_US.UTF-8
keyboard us
timezone US/Eastern
auth --useshadow --enablemd5
selinux --enforcing
firewall --enabled --service=mdns
repo --name=base    --baseurl=file://REPOPATH

xconfig --startxonboot
part / --size 4096 --fstype ext4
services --enabled=NetworkManager --disabled=network,sshd


%packages
syslinux
kernel
@base
@core
@basic-desktop
...
{% endcodeblock %}
#### Postinstallation stage:

Here the real mess is starting. Triple variable escaping is a pain:
    %post

    ## default LiveCD user
    LIVECD_USER="centoslive"

    ########################################################################
    # Create a sub-script so the output can be captured
    # Must change "$" to "\$" and "`" to "\`" to avoid shell quoting
    ########################################################################
    cat > /root/post-install << EOF_post
    #!/bin/bash

    echo ###################################################################
    echo ## Creating the livesys init script
    echo ###################################################################

Here is an example code snipplet from centos6-liveCD-desktop.cfg

{% codeblock centos6-liveCD-desktop.cfg lang:bash %}
%post
...

. /etc/init.d/functions

if ! strstr "\\\`cat /proc/cmdline\\\`" liveimg || [ "\\\$1" != "start" ]; then
      exit 0
      fi

      if [ -e /.liveimg-configured ] ; then
            configdone=1
            fi


            exists() {
                  which \\\$1 >/dev/null 2>&1 || return
                      \\\$*
                      }

...
{% endcodeblock %}

Maintaining your bash code is not convenient in such a way. The same goes for catching output or just plain debugging.
As as result adding your own software to the livecd becomes a laborious task ( in case you need more then just adding an individual package) 


Building LiveCD with Ansible
============================

Introduction
------------

{% codeblock lang:bash %}
.
├── roles                         # Ansible roles folder
│   ├── livecd-pre-common
│   ├── centos-sshd-service       # sshd service role
│   ├── epel-repo                 # epel repo setup
│   ├── livecd-pxe-common
│   ├── livecd-post-common
│   └── livecd-isolinux-common
├── templates
│   └── centos6-mini.ks.j2        # Basic config template
├── centos6-mini.yml              # Ansible Playbook for %post stage
├── generate_config.py            # Config file Generator
├── README.md
└── Vagrantfile
{% endcodeblock %}
