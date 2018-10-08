#!/bin/bash

sudo apt install git-all -y
apt install python3 -y
apt-get install curl -y
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install requests
git clone https://github.com/CrulQRL/SIsdis.git

nohup python3 /root/SIsdis/server.py &
