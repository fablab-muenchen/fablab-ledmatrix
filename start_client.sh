#!/bin/bash
SOURCE_DIR=$( dirname -- "$0"; )
cd $SOURCE_DIR
git pull
pip3 install -r requirements.txt
python3 main.py