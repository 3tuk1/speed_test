#!/bin/bash

python3 setup.py
nohup python3 speed_test2.py > speed_test2.log 2>&1 &
