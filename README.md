# School server - Ansible playbooks
Ansible playbooks for setting up and configuring a school's app server.

## Requirements
Install ansible first by following the official handbook:
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

After that you can install all ansible roles:

   ansible-galaxy install -r requirements.yml

## Commands
Useful ansible commands:

    ansible-inventory --list

    ansible schoolservers -m ping

    ansible-playbook initial-setup.yml

## Links

* Best practices for directory layout: https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#content-organization
* Real world example for complex Ansible setup: https://github.com/ct-Open-Source/telerec-t-base
