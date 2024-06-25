#!/usr/bin/env python3

import subprocess
import json

inputs = subprocess.check_output(['swaymsg', '-t', 'get_inputs'], universal_newlines=True)
inputs = json.loads(inputs)

touchpad = [x for x in inputs if x['type'] == 'touchpad']
touchpad_dwt_status = touchpad[0]['libinput']['dwt']

if touchpad_dwt_status == 'enabled':
    subprocess.run(['swaymsg', 'input', 'type:touchpad', 'dwt', 'disabled'])
else:
    subprocess.run(['swaymsg', 'input', 'type:touchpad', 'dwt', 'enabled'])
