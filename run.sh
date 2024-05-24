#!/bin/bash
apt update
apt upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
python -m bot.py