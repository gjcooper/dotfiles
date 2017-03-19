#!/usr/bin/env bash
#
# Installs things and then passes onto python for links etc

# Go to parent directory of script (usually /home/<user>/dotfiles) and save to var
cd "$(dirname "$0")/.."
DOTFILES_ROOT=$(pwd -P)

set -e # Exit immediately if non-zero exit status from command is detected
echo ''

# Install std software needed for 
install_sw () {
  # Use apt-get to install any misses pieces of the puzzle
  sudo -E apt-get -y install curl vim-nox gitk zsh tmux python3 ipython ipython3 dos2unix python-pip python3-pip i3 terminator suckless-tools lightdm dbus-x11 xsel dkms feh conky compton python3-venv python3-tk pandoc
  #Install flake8 for python 2 and 3
  sudo -E -H pip install flake8 pyflakes
  if [ -f /usr/local/bin/flake8 ]
  then
	  sudo mv /usr/local/bin/flake8{,.2}
  fi
  sudo -E -H pip3 install flake8 pyflakes
  if [ -f /usr/local/bin/flake8 ]
  then
	  sudo mv /usr/local/bin/flake8{,.3}
  fi
}

install_sw
python3 $DOTFILES_ROOT/scripts/managehome.py $DOTFILES_ROOT

echo ''
echo '  All installed!'
