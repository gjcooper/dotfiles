#!/usr/bin/env python3
import os
import subprocess
import re


icon = os.path.join(os.path.expanduser('~'), '.i3lock.png')
tmpbg = '/tmp/screen.png'

def	place_locks():
    '''Place lock images on the screen(s)'''
    # lockscreen image info
    icon_info = subprocess.check_output(['file', '-L', icon], universal_newlines=True)
    icon_x, icon_y = [int(res.strip()) for res in icon_info.split(',')[1].split('x')]

    xrandr_out = subprocess.check_output(['xrandr', '--query'], universal_newlines=True)
    connected_monitors = [x for x in
                          xrandr_out.splitlines()
                          if ' connected' in x]
    for mon in connected_monitors:
        try:
            dim = re.search('\d+x\d+[+]\d+[+]\d+', mon).group(0)
        except AttributeError:
            continue
        dim = dim.split('+', 1)
        res_x, res_y = [int(res) for res in dim[0].split('x')]
        off_x, off_y = [int(off) for off in dim[1].split('+')]
        p_x, p_y = off_x + res_x/2 - icon_x/2, off_y + res_y/2 - icon_y/2
        subprocess.call(['convert', tmpbg, icon, '-geometry',
                         '+{}+{}'.format(p_x, p_y), '-composite', '-matte',
                         tmpbg])

subprocess.call(['scrot', '-o', tmpbg])
subprocess.call(['convert', tmpbg, '-scale', '10%', '-scale', '1000%', tmpbg])
place_locks()
subprocess.call(['i3lock', '-i', tmpbg])
