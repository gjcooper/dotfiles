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
alias vend='deactivate'
alias coverr='coverage run --omit="venv/*" -m unittest discover && coverage report -m'
alias dvena='source ~/coding/venv/bin/activate'

# Functions
venl () {
	read -r -d '' USAGE <<- EOM
		venl [name]
		  [name] is the virtualenv to want to list the source packages for

		  if called without a name venl will list all virtualenvs in the home ~/.virtualenvs folder.
EOM
	if [[ $# == 0 ]]; then
		ls "${HOME}/.virtualenvs"
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

venm () {
	read -r -d '' USAGE <<- EOM
		venm [name] [location]
		  [name] is what you want to call the virtualenv and defaults to venv
		  [location] is where you want to store the virtualenv. Defaults to ~/.virtualenvs

		  venm will create a new python3 virtualenv, update pip and setuptools,
		  install pip-tools and wheel packages and activate the virtualenv ready to work.
EOM
	if [[ $# == 0 ]]; then
		name="venv"
		location=$(pwd)
	elif [[ $# == 1 ]]
	then
		if [[ $1 == "-h" ]]; then
			echo "$USAGE"
			return
		fi
		name=$1
		location="${HOME}/.virtualenvs"
	elif [[ $# == 2 ]];	then
		name=$1
		location=$2
	else
		echo "$USAGE"
		return
	fi
	python3 -m venv $location/$name
	vena "$location/$name"
	pip install -U pip
	pip install pip-tools
	pip install wheel
	pip install -U setuptools
}

vena () {
	read -r -d '' USAGE <<- EOM
		vena [name]
		  [name] is the virtualenv to activate, and default to venv

		  vena will search the local directory, and a ~/.virtualenvs directory for the virtualenv.
		  If your virtualenv is elsewhere pass a full path to the function.
EOM
	if [[ $# == 0 ]]; then
		name="venv"
	elif [[ $# == 1 ]];	then
		if [[ $1 == "-h" ]]; then
			echo "$USAGE"
			return
		fi
		name=$1
	else
		echo "$USAGE"
		return
	fi
	if [[ -d $name ]]; then
		source $name/bin/activate
	elif [[ -d "${HOME}/.virtualenvs/$name" ]]; then
		source "${HOME}/.virtualenvs/$name/bin/activate"
	else
		echo "Was not able to find the virtualenv"
		echo "$USAGE"
	fi
}
