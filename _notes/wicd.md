# Network Management with WICD

This guide gives instructions for how to use `wicd` for network management.

## Install

Install the following packages

- `wicd` (includes `wicd`, `wicd-cli`, `wicd-curses`)
- `wicd-gtk` (optional GUI client)

# Disable other services

The following services must be disabled:

- `wpa_supplicant`
- `dhcpcd`

To disable these, go to `/var/service` and delete the symlinks, such as

```sh
rm dhcpcd
```

**Do not** use `rmdir` or `rm -rf`.

# Setup

Make sure that the user trying to run the `wicd` client is in the `users` group
by running

```sh
usermod -aG users <USER>
```

If `users` does not exists, this will create it and append it to the groups of
`<USER>`.

Enable `wicd` by running

```sh
ln -s /etc/sv/wicd /var/service/
```

then reboot. The `wicd` daemon now runs at startup and can be used to connect
to networks.
