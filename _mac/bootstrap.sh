#!/usr/bin/env sh

#------------------------------------------------------------------------------
# Load default settings
#------------------------------------------------------------------------------

./settings.sh

#------------------------------------------------------------------------------
# Install brew
#------------------------------------------------------------------------------

if ! command -v brew > /dev/null; then
    url="https://raw.githubusercontent.com/Homebrew/install/master/install"
    /usr/bin/ruby -e "$(curl -fsSL "$url")"
fi

#------------------------------------------------------------------------------
# Install brew packages
#------------------------------------------------------------------------------

# Read in the package list
pkgs=""
pkgs_cask=""
taps=""
while read line; do
    # Skip empty lines
    if echo "$line" | egrep -q "^\s*$"; then
        # Do nothing
        echo Empty > /dev/null
    # Skip comments
    elif echo "$line" | egrep -q "^#"; then
        # Do nothing
        echo Comment > /dev/null
    # Find taps
    elif echo "$line" | egrep -q "^\\["; then
        tap="$(echo "$line" | sed "s/\\[\\(.*\\)\\]/\1/")"
        taps="$taps $tap"
    # Find packages
    else
        if [ -z "$taps" ]; then
            pkgs="$pkgs $line"
        else
            pkgs_cask="$pkgs_cask $line"
        fi
    fi
done < brew.packages

# Remove "cask" from $taps
old=$taps
taps=
for t in $old; do
    if [ "$t" != "-" ]; then
        taps="$taps $t"
    fi
done

# Install packages
[ -n "$pkgs" ]      && brew install $pkgs
[ -n "$taps" ]      && brew tap $taps
[ -n "$pkgs_cask" ] && brew cask install $pkgs_cask
