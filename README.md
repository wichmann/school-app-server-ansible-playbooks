# School server - Ansible playbooks
Ansible playbooks for setting up and configuring a school's app server. These
playbooks use Docker Compose scripts from [the Github repo "SchoolAppServer"](https://github.com/wichmann/SchoolAppServer).

## Requirements
Install ansible first by following the [official handbook](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html):

After that you can install all ansible roles:

    ansible-galaxy install -r requirements.yml

## Usage
First, you have to provide all necessary parameters and settings by editing the
files in the directories "group_vars" and "host_vars".

After that you can just run the main playbook to install and configure all
services:

    ansible-playbook site.yml

It is possible to run only roles with certain tags from a given playbook on chosen
hosts, e.g.:

    ansible-playbook infrastructure.yml --limit server-it-01 --tags "monitoring"

## Useful commands
Show full inventory with all variables:

    ansible-inventory --list

Try to log in to all servers in group:

    ansible schoolservers -m ping

Simple tasks can be executed manually as [ad hoc commands](https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html):

    ansible server-it-01 -a "/sbin/reboot" -u wichmann
    ansible server-it-01 -m ansible.builtin.copy -a "src=/etc/hosts dest=/tmp/hosts" -u wichmann
    ansible schoolservers -m ansible.builtin.apt -a "force_apt_get: true upgrade: dist" -u wichmann
    ansible schoolservers -a "sudo systemctl reload alloy" -u wichmann
    ansible schoolservers -m ansible.builtin.service -a "name=alloy state=reloaded" -u wichmann
    ansible all -m ansible.builtin.setup -u wichmann

## Links

* Best practices for directory layout: https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#content-organization
* Real world example for complex Ansible setup: https://github.com/ct-Open-Source/telerec-t-base
