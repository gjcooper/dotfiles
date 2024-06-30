#!/usr/bin/env python3
from pathlib import Path
import sys
import subprocess
import random
import time
import logging
logging.basicConfig(filename='randBG.log',level=logging.DEBUG)
logging.info('Script start')
bgdir = Path.home() / 'Pictures' / 'bgs'


def getonemon():
    """check whether one monitor (True) or Two (False)"""
    with open('/tmp/monitor_mode.dat') as monfile:
        mode = monfile.read().strip()
    return mode in {'EXTERNAL', 'INTERNAL'}


def looping(sleeptime):
    """Change the desktop BG every sleeptime minutes"""
    while True:
        bgpics = list(bgdir.iterdir())
        if getonemon():
            subprocess.call(['feh', '--auto-rotate', '--bg-fill', random.choice(bgpics)])
        else:
            subprocess.call(['feh', '--auto-rotate', '--bg-fill', random.choice(bgpics),
                '--auto-rotate', '--bg-fill', random.choice(promptpics)])
        time.sleep(60 * sleeptime)


if __name__ == '__main__':
    time_delay = 5 if (len(sys.argv) < 2) else float(sys.argv[1])
    logging.info('Ready to loop')
    looping(time_delay)
