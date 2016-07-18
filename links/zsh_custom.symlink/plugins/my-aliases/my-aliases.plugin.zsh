# Example aliases
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
alias p3='python3'
alias d2u='dos2unix'
alias apu='sudo apt-get update'
alias papu='sudo -E apt-get update'
alias apug='sudo apt-get upgrade'
alias papug='sudo -E apt-get upgrade'
alias gpall='git push -u origin --all && git push -u origin --tags'
compdef _git gpall=git-push
alias ip3='ipython3'
alias vena='source venv/bin/activate'
alias vend='deactivate'
