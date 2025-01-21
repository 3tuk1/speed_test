@echo off
python setup.py
start python speed_test2.py > speed_test2.log 2>&1
pause
