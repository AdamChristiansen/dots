#!/usr/bin/env sh

# This script modifies system settings to have the default behaviour.

# Disable DS_Store generation on network drives
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true

# Create a file that prevents terminals from printing a message at startup.
f="$HOME/.hushlogin"
if [ ! -f "$f" ]; then
    echo "This file prevents terminals printing a message on login" >> "$f"
fi
