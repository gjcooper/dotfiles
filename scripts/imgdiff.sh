#!/bin/bash

if [[ -f "$1" ]] && [[ -f "$2" ]]; then
  compare "$2" "$1" png:- | montage -geometry +4+4 "$2" - "$1" png:- | feh -
else
  if [[ -f "$1" ]]; then
    echo "+ Image Added"
    feh "$1"
  else
    echo "- Image Removed"
    feh "$2"
  fi
fi

exit 0
