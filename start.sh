#!/bin/bash
pkill -f servermanager.py
pip3 install -r requirements.txt --upgrade --no-deps --force-reinstall
sleep 5
python3 -u servermanager.py >> error.log 2>&1 &