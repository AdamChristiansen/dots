function __fish_command_not_found_handler --on-event fish_command_not_found
    printf "Oops, %s%s%s is an unknown command.\n" (set_color -u brred) \
        (string escape -- $argv[1]) (set_color normal) >&2
end
