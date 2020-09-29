# To maintain compatibility with non-POSIX shells like fish, this file should
# adhere to the following rules:
#
# - Empty lines are allowed
# - Lines containing only comments are allowed
# - Lines matching the form `export VAR=...` are allowed
#   - Note that there is no trailing comment allowed
# - Local (non-export) variables are not allowed
# - Simple variable interpolation like `$VAR` is allowed
#   - No other interpolations are allowed (like `${VAR}` and ${VAR:...}`)
#
# These rules are strict but useful, since the easiest way to load this file in
# shells like fish is to manually process it.

# Move Cargo directories out of home
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"
export PATH="$PATH:$XDG_DATA_HOME/cargo/bin"
