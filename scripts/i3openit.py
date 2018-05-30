#!/usr/bin/python

# i3openit.sh  
# E.g.
# i3openit.sh 5 firefox

import sys
import subprocess
import os

if len(sys.argv) < 3:
    print("Usage: i3openit.sh <workspace-number> <program-name> ")
    sys.exit(0)

workspace = sys.argv[1]
program = sys.argv[2:]

for n, p in enumerate(program):
    if os.path.isfile(p):
        program[n] = os.path.abspath(p)

workspacefull = workspace + ';'

print("Workspace: " + workspace, ", Program: ", program)
print(["i3-msg", "workspace", workspacefull, "exec"] + program)
subprocess.call(["i3-msg", "workspace", workspacefull, "exec"] + program)
