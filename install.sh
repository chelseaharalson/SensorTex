#!/bin/sh
apt-get update  # To get the latest package lists
apt-get install python-pip libatlas-base-dev gfortran python-dev build-essential g++ python-numpy python-scipy python-matplotlib python-imaging libc6-i386 -y
pip install progressbar
#etc.
