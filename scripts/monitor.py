#!/usr/bin/env python3
import os
import subprocess
import time
from contextlib import contextmanager
import logging
from pathlib import Path

logging.basicConfig(filename='monitor.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

HDMI_OUTPUT = "HDMI-1"
USBC_OUTPUT = "DP-2"
USBC_ALONE_OUTPUT = "DP-1"
INTERNAL_OUTPUT = "eDP-1"
outputs = [INTERNAL_OUTPUT, HDMI_OUTPUT, USBC_OUTPUT, USBC_ALONE_OUTPUT]
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
wait_time = 2
check_time = 5  # Time to wait before checking for a change in connected monitors


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
    logger.debug('CONNECTED: %s', connected)
    return connected


def get_file_state():
    """Look at file status to get connected monitors
    :returns: TODO

    """
    dirs = Path('/sys/devices/pci0000:00/0000:00:02.0/drm/card0/').glob('card0*')
    status_files = (p / 'status' for p in dirs)
    return [sf.read_text().strip() for sf in status_files]


def switch(mode, cmd, connected):
    """Switch modes and save current mode to a temp file"""
    cmd = cmd.format(*(connected + list(set(outputs) - set(connected))))
    logger.debug(xcmd_start + cmd)
    subprocess.call((xcmd_start + cmd).split())
    with open(mode_path, 'w') as monout:
        monout.write(mode)


def watch(mode):
    """watch the named pipe for any message"""
    # Reset on reboot/reload of settings to internal only
    monitor_state = 'IDLE'  # (or LOOK)
    mode, cmdend = monitor_modes[1]['INTERNAL']
    conn_outputs = [outputs[0]]
    switch(mode, cmdend, conn_outputs)
    start_time = 0
    _state_trace = get_file_state()
    with get_pipe(pipe_path) as pipe:
        while True:
            if monitor_state == 'LOOK':
                if time.time() - start_time > wait_time:
                    switch(mode, cmdend, conn_outputs)
                    monitor_state = 'IDLE'

            message = pipe.read()
            if message:
                logger.debug('[%s,%s]', mode, message)
                conn_outputs = connected()
                assert len(conn_outputs) <= 3
                try:
                    if 'S' in message:
                        mode, cmdend = monitor_modes[1]['INTERNAL']
                    else:
                        mode, cmdend = monitor_modes[len(conn_outputs)][mode]
                except KeyError:
                    mode, cmdend = monitor_modes[1]['INTERNAL']
                monitor_state = 'LOOK'
                subprocess.call(['notify-send', mode, '-t', '500'])
                start_time = time.time()
                time.sleep(0.1)
            elif time.time() - start_time > check_time:
                monitor_statuses = get_file_state()
                if monitor_statuses != _state_trace:
                    _state_trace = monitor_statuses
                    # Switch back to internal only
                    monitor_state = 'IDLE'  # (or LOOK)
                    mode, cmdend = monitor_modes[1]['INTERNAL']
                    switch(mode, cmdend, conn_outputs)
                start_time = time.time()
            else:
                time.sleep(0.25)


if __name__ == '__main__':
    watch(monitor_mode)
