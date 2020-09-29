# Wallpaper

This is where a wallpaper should be stored (if desired) to be found at WM
startup. The WM should run the `.config/wallpaper/lauch` script. A wallpaper
is set based on the following rules.

1.  If `$XDG_CONFIG_HOME/wallpaper/image/` contains an image, it will be used.
    Note that this directory can contain any number of `jpg` or `png` images,
    but only the first one returned by `ls` will be used. The file can be named
    anything.
2.  If a wallpaper image is found but there is an error setting it, proceed to
    the next step.
3.  If no wallpaper image is found, then the `_color_wall_hex` template value
    is used to set a solid color.

The `wallpaper-changer` script is a utility which is used to select a
wallpaper. The script prompts the user to select a wallpaper from an image
contained in a specific directory. It requires `sxiv` to be installed. The
first directory found from the following list is used:

1. The path of the passed in argument
2. `$XDG_PICTURES_DIR/Wallpaper`
3. `$HOME/Pictures/Wallpaper`

and the directory is recursively searched.
