#!/usr/bin/env python3
import os
import subprocess
import time
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

HDMI_OUTPUT = "HDMI-1"
USBC_OUTPUT = "DP-1"
INTERNAL_OUTPUT = "eDP-1"
monitor_mode = 'INTERNAL'
mode_list = ['INTERNAL', 'CLONED', 'LEFT', 'RIGHT', 'EXTERNAL']
xcmd_start = 'xrandr --output {} '.format(INTERNAL_OUTPUT)
two_monitor_modes = {
    'INTERNAL': ('CLONED', '--auto --output {} --auto --same-as {}'),
    'CLONED': ('LEFT', '--auto --output {} --auto --left-of {}'),
    'LEFT': ('RIGHT', '--auto --output {} --auto --right-of {}'),
    'RIGHT': ('EXTERNAL', '--off --output {} --auto'),
    'EXTERNAL': ('INTERNAL', '--auto --output $EXTERNAL_OUTPUT --off'),
}
one_monitor_modes = ('INTERNAL', '--auto --output {} --off --output {} --off')
pipe_path = "/tmp/monitor_pipe"
mode_path = '/tmp/monitor_mode.dat'


@contextmanager
def get_pipe(pipe_name):
    """Create a RDONLY, NONBLOCKING pipe and return a file object"""
    try:
        if os.path.exists(pipe_name):
            os.unlink(pipe_name)
        os.mkfifo(pipe_path)
        pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
        with os.fdopen(pipe_fd) as pipe:
            yield pipe
    finally:
        os.unlink(pipe_name)


def external():
    """Get the current external output"""
    xout = subprocess.check_output(['xrandr'], universal_newlines=True)
    for line in xout.splitlines():
        if line.startswith(HDMI_OUTPUT):
            if line.split()[1] == 'connected':
                return HDMI_OUTPUT
        if line.startswith(USBC_OUTPUT):
            if line.split()[1] == 'connected':
                return USBC_OUTPUT
    return ''


def switch(mode, cmd):
    """Switch modes and save current mode to a temp file"""
    logger.debug(xcmd_start + cmd)
    subprocess.call((xcmd_start + cmd).split())
    with open(mode_path, 'w') as monout:
        monout.write(mode)


def watch(mode):
    """watch the named pipe for any message"""
    # Reset on reboot/reload of settings
    mode, cmdend = one_monitor_modes
    switch(mode, cmdend.format(HDMI_OUTPUT, USBC_OUTPUT))
    with get_pipe(pipe_path) as pipe:
        while True:
            message = pipe.read()
            if message:
                logger.debug('[{},{}]', mode, message)
                ext = external()
                if not ext:
                    mode, cmdend = one_monitor_modes
                    switch(mode, cmdend.format(HDMI_OUTPUT, USBC_OUTPUT))
                else:
                    mode, cmdend = two_monitor_modes[mode]
                    switch(mode, cmdend.format(ext, INTERNAL_OUTPUT))
            else:
                time.sleep(0.5)


if __name__ == '__main__':
    watch(monitor_mode)
