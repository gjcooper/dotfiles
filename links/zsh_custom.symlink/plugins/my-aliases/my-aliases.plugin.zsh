# Example aliases
# Extra git aliases (on top of zsh standard ones)
alias gdt='git difftool'
compdef _git gdt=git-difftool
alias glc='git log --pretty=format:"%C(bold green)%h\\ %ad%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --date=relative'
compdef _git glc=git-log
alias glca='git log --pretty=format:"%C(bold green)%h\\ %ad%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --date=relative --all'
compdef _git glca=git-log
alias glga='git log --pretty=format:"%C(bold green)%h\\ %ad%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --date=relative --all --graph'
compdef _git glga=git-log
alias glgas='git log --pretty=format:"%C(bold green)%h\\ %ad%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --date=relative --all --graph --simplify-by-decoration'
compdef _git glga=git-log
alias glcd='git log --pretty=format:"%C(bold green)%h%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --numstat'
compdef _git glcd=git-log
alias gcheck='git ls-files -o'
compdef _git gcheck=git-ls-files
alias gpall='git push -u origin --all && git push -u origin --tags'
compdef _git gpall=git-push
#Shortenings
alias p3='python3'
alias d2u='dos2unix'
alias ip3='ipython3'
alias vend='pyenv deactivate'
alias vena='pyenv activate'
alias venrm='pyenv uninstall'
alias coverr='coverage run --omit="venv/*" -m unittest discover && coverage report -m'

# Functions
venm () {
	read -r -d '' USAGE <<- EOM
		venm [name]
		  [name] is the name of the virtualenv to create

		  The virtual environment is created in $WORKON_HOME and is created using `python -m venv`

		  This means the current version of python as returned by pyenv is used
EOM
	if [[ $# == 0 ]]; then
		echo "$USAGE"
		return
	elif [[ $# == 1 ]]; then
		name=$1
		version=$(pyenv version-name)
	elif [[ $# == 2 ]]; then
		version=$1
		name=$2
	else
		echo "$USAGE"
		return
	fi
	pyenv virtualenv $version $name
	vena $name
}

venl () {
	read -r -d '' USAGE <<- EOM
		venl [name]
		  [name] is the virtualenv to want to list the source packages for

		  if called without a name venl will list all virtualenvs in the $WORKON_HOME folder.
EOM
	if [[ $# == 0 ]]; then
		pyenv virtualenvs
		return
	elif [[ $# == 1 ]]; then
		name=$1
	else
		echo "$USAGE"
		return
	fi
	vena $name
	pip freeze
	vend
}

linx () {
	read -r -d '' USAGE <<- EOM
		linx [dir]
		  [dir] is the directory for which to list all links

		  if called without a dir linx will list all links in the current directory.
EOM
	if [[ $# == 0 ]]; then
		dir='.'
	elif [[ $# == 1 ]]; then
		dir=$1
	else
		echo "$USAGE"
		return
	fi
	find $dir -maxdepth 1 -type l -exec ls --color -d -l {} \;
}

hgrep () {fc -Dlim "*$@*" 1 }
