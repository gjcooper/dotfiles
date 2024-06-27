#!/usr/bin/env python3

import subprocess

def synclient_toggle_touchpad():
    synlist = subprocess.check_output(["synclient", "-l"], universal_newlines=True)
    for line in synlist.splitlines():
        if 'TouchpadOff' in line:
            state = line.split('=')[1].strip()
            break

    if state == '0':
        subprocess.call(['synclient', 'TouchpadOff=1'])
    else:
        subprocess.call(['synclient', 'TouchpadOff=0'])

def libinput_dwt():
    dev = 'SNSL0028:00 2C2F:0028 Touchpad'
    prop = 'libinput Disable While Typing Enabled'
    liblist = subprocess.check_output(['xinput', 'list-props', dev], universal_newlines=True)
    for line in liblist.splitlines():
        if prop in line:
            state = line.split()[-1].strip()
            break

    if state == '0':
        subprocess.call(['xinput', 'set-prop', dev, prop, '1'])
    else:
        subprocess.call(['xinput', 'set-prop', dev, prop, '0'])

try:
    synclient_toggle_touchpad()
except (FileNotFoundError):
    libinput_dwt()
