# Description #

* Install script based on bootstrap from holman/dotfiles (Github)
* All home directory symlinks to be stored in links

Latest run down of process:
Xubuntu 20.04 install into VirtualBox (i3 version)

* Grab desktop iso from source mirror
* Attach in virtualbox and boot
* Install, following prompts
* Choose minimal install
* install git, gcc, perl, make
* insert GuestAdditions cdrom and mount, sudo sh /media/cdrom/VBoxLinuxAdditions.run
* Copy SSH key to user home directory
* clone (via ssh) my dotfiles repo
* run dotfiles/scripts/managehome.py script: python3 managehome.py ~/dotfiles
* chsh gavin -s /bin/zsh
* link randBG script to /user/local/bin
