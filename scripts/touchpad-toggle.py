#!/usr/bin/env python3

import subprocess

synlist = subprocess.check_output(["synclient", "-l"], universal_newlines=True)
for line in synlist.splitlines():
    if 'TouchpadOff' in line:
        state = line.split('=')[1].strip()
        break

if state == '0':
    subprocess.call(['synclient', 'TouchpadOff=1'])
else:
    subprocess.call(['synclient', 'TouchpadOff=0'])
