#!/usr/bin/env python3
import os
import sys
import subprocess
import random
import time
import logging
logging.basicConfig(filename='randBG.log',level=logging.DEBUG)
logging.info('Script start')
picdir = os.path.join(os.path.expanduser('~'), 'Pictures')
bgdir = os.path.join(picdir, 'bgs')
promptdir = os.path.join(picdir, 'prompts')


def getonemon():
    """check whether one monitor (True) or Two (False)"""
    with open('/tmp/monitor_mode.dat') as monfile:
        mode = monfile.read().strip()
    return mode in {'EXTERNAL', 'INTERNAL'}


def getpics(*dirs):
    """return list of suitable pics from dir provided"""
    piclists = []
    for picdir in dirs:
        piclists.append([os.path.join(picdir, f) for f in os.listdir(picdir) if f.endswith('.jpg')])
    return piclists


def looping(sleeptime):
    """Change the desktop BG every sleeptime minutes"""
    while True:
        bgpics, promptpics = getpics(bgdir, promptdir)
        if getonemon():
            subprocess.call(['feh', '--auto-rotate', '--bg-fill', random.choice(bgpics)])
        else:
            if random.choice([0, 1]):
                subprocess.call(['feh', '--auto-rotate', '--bg-fill', random.choice(bgpics),
                                 '--auto-rotate', '--bg-fill', random.choice(promptpics)])
            else:
                subprocess.call(['feh', '--auto-rotate', '--bg-fill', random.choice(promptpics),
                                 '--auto-rotate', '--bg-fill', random.choice(bgpics)])
        time.sleep(60 * sleeptime)


if __name__ == '__main__':
    time_delay = 5 if (len(sys.argv) < 2) else float(sys.argv[1])
    logging.info('Ready to loop')
    looping(time_delay)
