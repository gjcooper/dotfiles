#!/bin/bash
if [ "$1" = "-c" ]; then
    autorandr --cycle
elif [ "$1" = "-s" ]; then
    autorandr solo
fi
sleep 0.5
notify-send -t 1500 "Monitor Mode" "$(autorandr --current)"
