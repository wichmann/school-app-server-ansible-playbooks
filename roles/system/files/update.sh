#!/usr/bin/env bash

# Update des gesamten Servers
# Autor: Christian Wichmann
# Datum: 2024-06-06

# Check if user is root (https://stackoverflow.com/a/18216122/18073555)
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo
echo "*** Aktualisiere Pakete und Docker Container... ***"
echo

apt update
apt full-upgrade -y

#docker image prune -a -f
