# Description #

* Install script based on bootstrap from holman/dotfiles (Github)
* All home directory symlinks to be stored in links

Latest run down of process:
Debian Testing install into VirtualBox (i3 version)

* Grab mini.iso from source mirror
* Attach in virtualbox and boot
* Install, following prompts
* Do not install Desktop Environment
* install git
* clone (via https) my dotfiles repo
* run dotfiles/scripts/setup.sh script
* insert GuestAdditions cdrom and mount, sudo sh /media/cdrom/VBoxLinuxAdditions.run
* chsh gavin -s /bin/zsh
* add contrib, non-free to sources.list
* generate machine specific key, add to lastpass etc
