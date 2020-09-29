# Temporary File System

`tmpfs` creates a filesystem in RAM. This is advantageous for a few reasons:

* Performance: No disk access.
* Power: Enhanced battery life.
* Security: Files are not writtent to the disk.
* Reliability: SSDs experience fewer write cycles.

`/tmp` is commonly set up as `tmpfs`. To set up `/tmp` as `tmpfs`, add the
following entry to `/etc/fstab`:

```
tmpfs /tmp tmpfs defaults,nodev,nosuid 0 0
```

This will create a `tmpfs` with the default settings that uses up to half of
the available memory (because no size option was set). Note that this does not
immediately allocate half of memory, it only uses memory as needed.

For higher granularity control, something like the following can be used.

```
tmpfs /tmp tmpfs mode=1777,noatime,nodev,nosuid,rw,size=1G 0 0
```

The option `noatime` is likely safe, since generally `mtime` is used and
`strictatime` is rarely enabled (also, `atime` is not that useful anyway).

## Temporary Resize

A `tmpfs` can be resized without reboot by using a command like the following:

```shell
mount -o remount,size=2G /tmp
```
