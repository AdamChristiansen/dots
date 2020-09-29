# Keyring

This uses the `gnome-keyring`, so make sure it is installed. Even though it is
the _GNOME_ keyring, it can be used outside of GNOME with the right
configuration.

To view keys, use a program like `seahorse`.

## Instructions

1.  Install `gnome-keyring`
2.  We want to start the keyring with PAM at login.
    1.  Open `/etc/pam.d/login` and add:

        ```sh
        # Add at the end of the "auth" section
        auth       optional     pam_gnome_keyring.so

        # Add at the end of the "session" section
        session    optional     pam_gnome_keyring.so auto_start
        ```
    2.  Open `/etc/pam.d/passwd` and add:

        ```sh
        # Add at the end of the "password" section
        password optional pam_gnome_keyring.so
        ```
3.  The `gnome-keyring-daemon` needs to be initialized after being started by
    PAM, so add this somewhere to a login shell, like `~/.xinitrc`:

    ```sh
    # Start the keyring
    if command -v gnome-keyring-daemon; then
        eval $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,keyring)
        export SSH_AUTH_SOCK
    fi
    ```

## A note about SSH keys

SSH keys generated with the `-o` option cannot be unlocked by the keyring, and will give an error like:

```
sign_and_send_pubkey: signing failed: agent refused operation
```

Instead, generate keys with

```sh
ssh-keygen -t rsa -b 4096 -C "email@example.com"
```
