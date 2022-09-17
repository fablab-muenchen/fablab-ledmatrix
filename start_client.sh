#!/bin/bash
SOURCE_DIR=$( dirname -- "$0"; )
cd $SOURCE_DIR
git pull
python3 main.py