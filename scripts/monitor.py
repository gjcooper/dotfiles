#!/usr/bin/env python3
import os
import subprocess
import time
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

HDMI_OUTPUT = "HDMI-1"
USBC_OUTPUT = "DP-2"
INTERNAL_OUTPUT = "eDP-1"
outputs = [INTERNAL_OUTPUT, HDMI_OUTPUT, USBC_OUTPUT]
monitor_mode = 'INTERNAL'
xcmd_start = 'xrandr '
monitor_modes = {
    1: {'INTERNAL': ('INTERNAL', '--output {0} --auto --output {1} --off --output {2} --off')},
    2: {'INTERNAL': ('RIGHT', '--output {0} --auto --output {1} --auto --right-of {0}'),
        'RIGHT': ('LEFT', '--output {0} --auto --output {1} --auto --left-of {0}'),
        'LEFT': ('CLONED', '--output {0} --auto --output {1} --auto --same-as {0}'),
        'CLONED': ('EXTERNAL', '--output {0} --off --output {1} --auto'),
        'EXTERNAL': ('INTERNAL', '--output {0} --auto --output {1} --off'), },
    3: {'INTERNAL': ('LAB', '--output {0} --auto --output {1} --auto --right-of {0} --output {2} --auto --right-of {1}'),
        'LAB': ('DUAL', '--output {0} --off --output {1} --auto --output {2} --auto --right-of {1}'),
        'DUAL': ('INTERNAL', '--output {0} --auto --output {1} --off --output {2} --off'), }}
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


def connected():
    """Get the current connected output(s)"""
    xout = subprocess.check_output(['xrandr'], universal_newlines=True)
    connected = []
    for output in outputs:
        for line in xout.splitlines():
            if line.startswith(output):
                if line.split()[1] == 'connected':
                    connected.append(output)
    return connected


def switch(mode, cmd):
    """Switch modes and save current mode to a temp file"""
    logger.debug(xcmd_start + cmd)
    subprocess.call((xcmd_start + cmd).split())
    with open(mode_path, 'w') as monout:
        monout.write(mode)


def watch(mode):
    """watch the named pipe for any message"""
    # Reset on reboot/reload of settings to internal only
    mode, cmdend = monitor_modes[1]['INTERNAL']
    switch(mode, cmdend.format(*outputs))
    with get_pipe(pipe_path) as pipe:
        while True:
            message = pipe.read()
            if message:
                logger.debug('[{},{}]', mode, message)
                conn_outputs = connected()
                assert len(conn_outputs) <= 3
                try:
                    mode, cmdend = monitor_modes[len(conn_outputs)][mode]
                except KeyError:
                    mode, cmdend = monitor_modes[1]['INTERNAL']
                switch(mode, cmdend.format(*outputs))
                time.sleep(0.5)
            else:
                time.sleep(0.25)


if __name__ == '__main__':
    watch(monitor_mode)
