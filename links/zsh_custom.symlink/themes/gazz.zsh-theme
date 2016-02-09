local return_code="%(?..%{$fg[red]%}%? ↵%{$reset_color%})"

PROMPT='%m%{${fg_bold[magenta]}%}::%{$reset_color%}%{${fg[green]}%}%2~ ->%{${reset_color}%} '

RPROMPT='$(vi_mode_prompt_info) $(git_prompt_info) %F{blue}[%D %*] ${return_code}%{${reset_color}%}'

ZSH_THEME_GIT_PROMPT_PREFIX="%F{green}<%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[green]%}%{$fg[yellow]%}⚡%{$fg[green]%}>%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%}>"

MODE_INDICATOR="%{$fg_bold[magenta]%}<%{$reset_color%}%{$fg[magenta]%}<<%{$reset_color%}"

# TODO, make colour naming consistent
