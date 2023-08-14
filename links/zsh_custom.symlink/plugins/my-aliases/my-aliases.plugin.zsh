# Extra git aliases (on top of zsh standard ones)
alias gdt='git difftool'
compdef _git gdt=git-difftool
alias gmt='git mergetool'
compdef _git gmt=git-mergetool
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
# AWS/Service Workbench helpers
alias start_prefnorm='$HOME/swb/start-session.sh gjc216 278440638476 i-073e794196e1e5158'
alias start_prefred='$HOME/swb/start-session.sh gjc216 278440638476 i-068dc8f24099951a4'
alias start_prefredmore='$HOME/swb/start-session.sh gjc216 278440638476 i-0cfc3bc49eaa1b503'
alias start_prefneg='$HOME/swb/start-session.sh gjc216 278440638476 i-08d606d21d6da4f96'
alias aws_copymode='$HOME/swb/assume-role.sh gjc216 418071489834'


aws_list () {
	read -r -d '' USAGE <<- EOM
		aws_list workspace_name
		  workspace_name is the name of the workspace to list egress files for, and
      is required
EOM
  
  if [[ $# -ne 1 ]]; then
    echo $USAGE >&2
    exit 2
  fi

  prefnorm="a54ee996-563b-4c56-8235-62c510f0aa60"
  prefred="189fa174-3bd8-40c0-a722-d93c41c19ea0"
  prefredmore="75179041-495c-4708-b9b5-024ab7a0342f"
  prefneg="7ddf4dcb-8206-405c-a0f6-178b8a75c6c3"

  if [[ $1 == "prefnorm" ]]; then
    aws s3 ls s3://418071489834-prod-syd-uonswb-egress-store/$prefnorm/
  elif [[ $1 == "prefred" ]]; then
    aws s3 ls s3://418071489834-prod-syd-uonswb-egress-store/$prefred/
  elif [[ $1 == "prefredmore" ]]; then
    aws s3 ls s3://418071489834-prod-syd-uonswb-egress-store/$prefredmore/
  elif [[ $1 == "prefneg" ]]; then
    aws s3 ls s3://418071489834-prod-syd-uonswb-egress-store/$prefneg/
  else
    echo "Unrecognised instance name"
  fi
}

aws_cp () {
	read -r -d '' USAGE <<- EOM
		aws_list workspace_name filename dest
		  workspace_name is the name of the workspace to copy egress files from
      filename is the name of the file to download from the s3 bucket
      dest is the destination name/location to send the file to

    All arguments are required
EOM
  
  if [[ $# -ne 3 ]]; then
    echo $USAGE >&2
    return
  fi

  wks=$1
  src=$2
  dest=$3

  prefnorm="a54ee996-563b-4c56-8235-62c510f0aa60"
  prefred="189fa174-3bd8-40c0-a722-d93c41c19ea0"
  prefredmore="75179041-495c-4708-b9b5-024ab7a0342f"
  prefneg="7ddf4dcb-8206-405c-a0f6-178b8a75c6c3"

  if [[ $wks == "prefnorm" ]]; then
    aws s3 cp s3://418071489834-prod-syd-uonswb-egress-store/$prefnorm/$src $dest
  elif [[ $wks == "prefred" ]]; then
    aws s3 cp s3://418071489834-prod-syd-uonswb-egress-store/$prefred/$src $dest
  elif [[ $wks == "prefredmore" ]]; then
    aws s3 cp s3://418071489834-prod-syd-uonswb-egress-store/$prefredmore/$src $dest
  elif [[ $wks == "prefneg" ]]; then
    aws s3 cp s3://418071489834-prod-syd-uonswb-egress-store/$prefneg/$src $dest
  else
    echo "Unrecognised instance name"
  fi
}

aws_sync () {
	read -r -d '' USAGE <<- EOM
		aws_sync workspace_name dest <aws s3 sync options>
		  workspace_name is the name of the workspace to copy egress files from
      dest is the destination name/location to send the files to
      other aws s3 sync options are able to be passed on to the aws cli, such as --exclude="*old*

    All arguments except for the options for sync are required
EOM
  
  if [[ $# -lt 2 ]]; then
    echo $USAGE >&2
    return
  fi

  wks=$1
  dest=$2

  prefnorm="a54ee996-563b-4c56-8235-62c510f0aa60"
  prefred="189fa174-3bd8-40c0-a722-d93c41c19ea0"
  prefredmore="75179041-495c-4708-b9b5-024ab7a0342f"
  prefneg="7ddf4dcb-8206-405c-a0f6-178b8a75c6c3"

  echo "${@:3}"

  if [[ $wks == "prefnorm" ]]; then
    aws s3 sync s3://418071489834-prod-syd-uonswb-egress-store/$prefnorm/ $dest "${@:3}"
  elif [[ $wks == "prefred" ]]; then
    aws s3 sync s3://418071489834-prod-syd-uonswb-egress-store/$prefred/ $dest "${@:3}"
  elif [[ $wks == "prefredmore" ]]; then
    aws s3 sync s3://418071489834-prod-syd-uonswb-egress-store/$prefredmore/ $dest "${@:3}"
  elif [[ $wks == "prefneg" ]]; then
    aws s3 sync s3://418071489834-prod-syd-uonswb-egress-store/$prefneg/ $dest "${@:3}"
  else
    echo "Unrecognised instance name"
  fi
}

# Functions
venm () {
	read -r -d '' USAGE <<- EOM
		venm version name
		  name is the name of the virtualenv to create, and is required
		  version is the version of python (provided by > pyenv versions)

		  The virtual environment is created in $WORKON_HOME
EOM
	if [[ $# == 2 ]]; then
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
