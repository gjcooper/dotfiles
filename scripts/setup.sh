#!/usr/bin/env bash
#
# bootstrap installs things.

cd "$(dirname "$0")/.."
DOTFILES_ROOT=$(pwd -P)

set -e # Exit immediately if non-zero exit status from command is detected
echo ''

# Helper functions
install_sw () {
  # Use apt-get to install any misses pieces of the puzzle
  sudo -E apt-get -y install curl vim gitk zsh tmux python3 ipython ipython3 dos2unix python-pip python3-pip
  #Install flake8 for python 2 and 3
  sudo -E pip install flake8 pyflakes
  if [ -f /usr/local/bin/flake8 ]
  then
	  sudo mv /usr/local/bin/flake8{,.2}
  fi
  sudo -E pip3 install flake8 pyflakes
  if [ -f /usr/local/bin/flake8 ]
  then
	  sudo mv /usr/local/bin/flake8{,.3}
  fi
#  sudo -E pip3 install flake8
}

info () {
  printf "\r  [ \033[00;34m..\033[0m ] $1\n"
}

user () {
  printf "\r  [ \033[0;33m??\033[0m ] $1\n"
}

success () {
  printf "\r\033[2K  [ \033[00;32mOK\033[0m ] $1\n"
}

fail () {
  printf "\r\033[2K  [\033[0;31mFAIL\033[0m] $1\n"
  echo ''
  exit
}

setup_gitconfig () {
  if ! [ -f links/gitconfig.symlink ]
  then
    info 'setup gitconfig'
    git_credential='cache'
    user ' - What is your git author name?'
    read -e git_authorname
    user ' - What is your git author email?'
    read -e git_authoremail
    sed -e "s/AUTHORNAME/$git_authorname/g" -e "s/AUTHOREMAIL/$git_authoremail/g" -e "s/GIT_CREDENTIAL_HELPER/$git_credential/g" links/gitconfig.symlink.base > links/gitconfig.symlink
    success 'gitconfig'
  fi
}

setup_pypirc () {
  if ! [ -f links/pypirc.symlink ]
  then
    info 'setup pypirc'
	user ' - What is your pypi user name?'
    read -e pypi_username
	user ' - What is your pypi password?'
    read -e pypi_passwd
	user ' - What is your testpypi user name?'
    read -e tpypi_username
	user ' - What is your testpypi password?'
    read -e tpypi_passwd
    sed -e "s/PYPI_USERNAME/$pypi_username/g" -e "s/PYPI_PASSWD/$pypi_passwd/g" -e "s/TEST_USERNAME/$tpypi_username/g" -e "s/TEST_PASSWD/$tpypi_passwd/g" links/pypirc.symlink.base > links/pypirc.symlink
    success 'pypirc'
  fi
}

setup_dircolors () {
  if ! [ -d $DOTFILES_ROOT/local/dircolors ]
  then
    git clone https://github.com/seebi/dircolors-solarized.git $DOTFILES_ROOT/local/dircolors
    user ' - What is your preferred colour scheme? (dark/light)'
    read -e dircolors_scheme
    if [ "$dircolors_scheme" == "dark" ]
    then
      ln -s $DOTFILES_ROOT/local/dircolors/dircolors.ansi-dark ~/.dircolors
    elif [ "$dircolors_scheme" == "light" ]
    then
      ln -s $DOTFILES_ROOT/local/dircolors/dircolors.ansi-light ~/.dircolors
    else
      fail "Colour scheme not recognised"
    fi
    success 'dircolors'
  fi
}

link_file () {
  local src=$1 dst=$2

  local overwrite= backup= skip=
  local action=

  if [ -f "$dst" -o -d "$dst" -o -L "$dst" ]
  then
    if [ "$overwrite_all" == "false" ] && [ "$backup_all" == "false" ] && [ "$skip_all" == "false" ]
    then
      local currentSrc="$(readlink $dst)"
      if [ "$currentSrc" == "$src" ]
      then
        skip=true;
      else
        user "File already exists: $dst ($(basename "$src")), what do you want to do?\n\
        [s]kip, [S]kip all, [o]verwrite, [O]verwrite all, [b]ackup, [B]ackup all?"
        read -n 1 action
        case "$action" in
          o )
            overwrite=true;;
          O )
            overwrite_all=true;;
          b )
            backup=true;;
          B )
            backup_all=true;;
          s )
            skip=true;;
          S )
            skip_all=true;;
          * )
            ;;
        esac
      fi
    fi
    overwrite=${overwrite:-$overwrite_all}
    backup=${backup:-$backup_all}
    skip=${skip:-$skip_all}

    if [ "$overwrite" == "true" ]
    then
      rm -rf "$dst"
      success "removed $dst"
    fi

    if [ "$backup" == "true" ]
    then
      mv "$dst" "${dst}.backup"
      success "moved $dst to ${dst}.backup"
    fi

    if [ "$skip" == "true" ]
    then
      success "skipped $src"
    fi
  fi

  if [ "$skip" != "true" ]  # "false" or empty
  then
    ln -s "$1" "$2"
    success "linked $1 to $2"
  fi
}

install_dotfiles () {
  info 'Installing dotfiles'
  local overwrite_all=false backup_all=false skip_all=false
  for src in $(find -H "$DOTFILES_ROOT/links" -maxdepth 1 -name '*.symlink')
  do
    echo $src
    dst="$HOME/.$(basename "${src%.*}")"
    link_file "$src" "$dst"
  done
}

setup_vim () {
  #Setup Vundle and source 
  info 'Installing vim bundles'
  if [ ! -d ~/.vim/bundle/Vundle.vim ]
  then
    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
  else
    info 'Vundle.vim already in .vim dir'
  fi
  vim +PluginInstall +qall
}

setup_ohmyzsh () {
  info 'Installing ohmyzsh'
  if [ ! -d ~/.oh-my-zsh ]
  then
    git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
  else
    info 'oh-my-zsh directory already found in home dir'
  fi
}
 
install_sw
setup_gitconfig
setup_pypirc
setup_dircolors
install_dotfiles
setup_vim
setup_ohmyzsh

echo ''
echo '  All installed!'
