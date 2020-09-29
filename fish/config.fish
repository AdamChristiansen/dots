# Sources export statements from a file, like ~/.profile
function __source_profile -a file
    if [ -f $file ]
        egrep "^export " $file | while read expr
            # Get the variable name and value
            set -l var   (echo $expr | sed -E "s/^export ([a-zA-Z_][a-zA-Z_0-9]+)=(.*)\$/\1/")
            set -l value (echo $expr | sed -E "s/^export ([a-zA-Z_][a-zA-Z_0-9]+)=(.*)\$/\2/")
            # Remove surrounding quotes (if any)
            set value (echo $value | sed -E "s/^\"(.*)\"\$/\1/")
            # Set the variable
            if [ $var = "PATH" ]
                # Split the components of the path, and add each path to
                # $fish_user_paths. The order of whether the paths are
                # prepended or appended to the $PATH are not preserved. They
                # will be added to $fish_user_paths in the order they appear
                # in the file
                for v in (string split ":" $value)
                    if [ $v != "\$PATH" ]
                        # Expand the path in case it contains $HOME, and only
                        # add the path if it does not already exist.
                        set -l path (eval echo $v)
                        if not contains $path $PATH \
                                && not contains $path $fish_user_paths
                            set -Ua fish_user_paths $path
                        end
                    end
                end
            else
                # Evaluate the variable in case it contains other variables
                set -gx $var (eval echo $value)
            end
        end
    end
end

# Load all config files
__source_profile ~/.profile
set -l profiled ~/.local/etc/profile.d
if [ -d $profiled ]
    for f in (ls $profiled)
        __source_profile $profiled/$f
    end
end
set -e profiled

# Bootstrap install fisher if it does not exist
set -q XDG_CONFIG_HOME; or set XDG_CONFIG_HOME ~/.config
set -gx fisher_path $XDG_CONFIG_HOME/fish/fisher
set fish_function_path $fish_function_path[1] \
    $fisher_path/functions $fish_function_path[2..-1]
set fish_complete_path $fish_complete_path[1] \
    $fisher_path/completions $fish_complete_path[2..-1]
for file in $fisher_path/conf.d/*.fish
    builtin source $file 2> /dev/null
end
if not functions -q fisher
    curl https://git.io/fisher --create-dirs -sLo \
        $XDG_CONFIG_HOME/fish/functions/fisher.fish
    fish -c fisher
end

# https://github.com/decors/fish-colored-man settings
set -gx man_blink -o red
set -gx man_bold -o green
set -gx man_standout -o yellow
set -gx man_underline -u brcyan

# Shell colors
set -gx fish_color_autosuggestion  black
set -gx fish_color_cancel          -r
set -gx fish_color_command         --bold
set -gx fish_color_comment         black
set -gx fish_color_cwd             green
set -gx fish_color_cwd_root        red
set -gx fish_color_end             brmagenta
set -gx fish_color_error           brred
set -gx fish_color_escape          bryellow --bold
set -gx fish_color_history_current --bold
set -gx fish_color_host            normal
set -gx fish_color_match           --background=brblue
set -gx fish_color_normal          normal
set -gx fish_color_operator        bryellow
set -gx fish_color_param           cyan
set -gx fish_color_quote           yellow
set -gx fish_color_redirection     brblue
set -gx fish_color_search_match    bryellow --background=brblack
set -gx fish_color_selection       white --bold --background=brblack
set -gx fish_color_user            brgreen
set -gx fish_color_valid_path      --underline

# Set the default editor
set -gx EDITOR     nvim
set -gx VISUAL     $EDITOR
set -gx GIT_EDITOR $EDITOR

# Abbreviations
abbr -ga ga   git add -A
abbr -ga gb   git branch
abbr -ga gc   git commit
abbr -ga gcm  git commit -m
abbr -ga gd   git diff
abbr -ga gch  git checkout
abbr -ga gl   git log
abbr -ga glg  git log --graph --oneline
abbr -ga gp   git push
abbr -ga gpl  git pull --rebase
abbr -ga gr   git reset
abbr -ga grh  git reset HEAD
abbr -ga gs   git status --short -u
abbr -ga let  set -l
abbr -ga mux  tmuxinator
abbr -ga muxc tmuxinator start code -n
abbr -ga muxd tmuxinator start default -n
abbr -ga ta   tmux attach-session -t
abbr -ga tl   tmux list-sessions
abbr -ga tn   tmux new -s
abbr -ga zat  zathura --fork

# Aliases
if type -q ranger
    alias r 'ranger'
end
if type -q rg
    alias rq 'rg --no-ignore --hidden --follow --glob "!.git/*"'
end
if type -q exa
    alias x  'exa'
    alias xa 'exa --git -a'
    alias xl 'exa --git -al'
    alias xt "exa --git -alT --ignore-glob='.git'"
end
if type -q xclip
    alias yy 'xclip -selection clipboard'
else if type -q pbcopy
    alias yy 'pbcopy'
end
alias yc 'printf "" | yy'

# Start the vi bindings
fish_vi_key_bindings insert
