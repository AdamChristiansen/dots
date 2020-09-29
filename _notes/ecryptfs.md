# Private Directory

A private encrypted directory mounted to `~/Private` can be created using
`ecryptfs-utils`.

Run `ecryptfs-setup-private` to create the following files and directories:

* `~/.ecryptfs/auto-mount`: If this file exists, `ecryptfs` will automatically
  mount the private directory at login.
* `~/.ecryptfs/auto-umount`: If this file exists, `ecryptfs` will automatically
  unmount the private directory at logout.
* `~/.ecryptfs/Private.sig`: A file containing signature of mountpoint
  passphrase.
* `~/.ecryptfs/Private.mnt`: A file containing path of the private directory
  mountpoint
* `~/.ecryptfs/wrapped-passphrase`: A file containing the mount passphrase,
  wrapped with the login passphrase
* `~/.ecryptfs/wrapping-independent`: This file exists if the wrapping
  passphrase is independent from login passphrase.
* `~/.Private`: The underlying directory containing encrypted data.
* `~/Private`: The mountpoint containing decrypted data (when mounted).

At login/logout, the default is that `~/Private` is automatically
mounted/unmounted.

**Always modify `~/Private` and not `~/.Private`.**

## Manual Mounting/Unmounting

Use `ecryptfs-mount-private` to manually mount the private directory. The
password is required.

Use `ecryptfs-umount-private` manually unmount the private directory.

## Automatic Mounting

Configure `pam` to automatically mount the encrypted directory by adding

```pamconf
auth            optional        pam_ecryptfs.so unwrap
session         optional        pam_ecryptfs.so unwrap
password        optional        pam_ecryptfs.so unwrap
```

to `/etc/pam.d/login`. This will automatically mount the directories after the
login password is entered.

## Changing Login Passphase

When the login passphrase is modified, be sure to update the wrapped
passphrase using `ecryptfs-rewrap-passphrase`.

```sh
ecryptfs-rewrap-passphrase "$HOME/.ecryptfs/wrapped-passphrase"
```

This will prompt for the old passphrase and then a new one can be entered. The
command unwraps the wrapped passphrase using the old passphrase and wraps it
with the new one. It is useful for when the login passphrase is changed and the
wrapped passphrase needs to be updated.
