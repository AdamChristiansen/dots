# Dots

My dot file management system.

* Configurations for a particular program or service are stored in a subdirectory
* The subdirectory naming conventions:
  * Subdirectories starting with `[a-z]` contain files which can be
    automatically installed on the system
  * Subdirectories starting with `_` contain files that are not automatically
    installed on the system (which require extra work) and anything else, such
    as notes
* Files can be marked as templates, which is a simple preprocessor type system
* Files can be executable when installed on the system

## Building and Installing

The script `dots.py` is a program which is used to build dot files and install
them on the system. The basic usage is:

```sh
python3 dots.py -v install <package> [packages]
```

To see the available commands, run:

```sh
python3 dots.py --help
```

It is recommended to install this in the path somewhere with a symbolic link:

```fish
# In fish, this looks like
ln -s (realpath dots.py) $HOME/.local/bin/dots
```

and now it can be invoked from anywhere with `dots`.

## Configuration

The configuration settings go in `dots.json`, which contains an object with the
following:

* `build` (object): The build settings.
  * `dir` (string, default: `"build"`): The build directory path.
  * `format` (boolean, default: `true`): Keep the configuration file nicely
    formatted.
* `packages` (object, default: `{}`): The packages that can be installed on the
  system. The keys are package names and the values are package objects.
* `templates` (object): The templating settings.
  * `begin` (string, default: `{{{`): The template interpolation beginning
    token.
  * `end` (string, default: `}}}`): The template interpolation ending token.
  * `include` (list, default: `[]`): A list of include objects.
  * `snippets` (string, default: `"snippets"`): The snippets directory path.
  * `variables` (object, default: `{}`): Values that are used to fill in
    templates. Both keys and values must be strings.

Package objects may contain the following:

* `files` (object, default: `{}`): The files that are installed as part of the
  package. The keys are the path to the file, and the value can be a string
  containing the destination (with environment variables) or an object
  containing the following:
  * `dest` (string, default: `null`): The path to the destination. This can be
    null to specify a build only product.
  * `executable` (boolean, default: `false`): Make the file executable when
    installed.
  * `template` (boolean, default: `false`): Fill in the file as a template.

The `templates.include` is a list of include objects, which can contain the
following:

* `path` (str): The path to the include file.
* `optional` (boolean, default: `false`): The file must exist at the specified
  path.

Alternatively, instead of an object, and include can be specified as a string
which will be the `path` value and `optional` will be set to `false`.

Both includes and snippets are used to define variables in other files. They
each serve two different purposes.

**Includes** are mixed into the variables before snippets, and overwrite any
variables that are already defined. An include is a JSON file with one object
containing a string to string mapping. They are applied in the order that they
are declared. Includes are useful for defining secret data or data that changes
from machine to machine and should not be tracked by a version control system.

**Snippets** are mixed into the variables after includes, and overwrite any
variables that are already defined. An include can be any type of file. The key
used is the basename of the file with all extensions stripped, and the value is
the file contents. This is useful for defining long variables.

## Templates

The templating system allows for files to be filled in from a common set of
variables to ensure that the same configurations are used across programs. This
can be used build config files that all use the same colors and fonts, for
example.

When a template is filled in, a search is done to find text in the template
between `templates.begin` and `templates.end` delimiters. The text inside must
be a valid Python expression, and most often, it is just a variable name. All
of the variables in `templates.variables` included as local variables, but have
an `_` prepended to them.

For example, suppose that the following variables are defined:

```json
{
  "font_name": "Iosevka",
  "font_size": "11"
}
```

Then can then be used in a template with:

```conf
font_normal = {{{ _font_name }}} {{{ _font_size }}}
font_large  = {{{ _font_name }}} {{{ int(_font_size) + 3 }}}
```

which will produce:

```conf
font_normal = Iosevka 11
font_large  = Iosevka 14
```

## Required Template Variables

This dotfile configuration requires the following template files to be created
offline that define the following:

* `local-os.json`:
  * `os`: Can be `linux` or `mac`
* `local-secret.json`:
  * `secret_git_name`: The full name to use as the git author
  * `secret_git_email`: The email address to use for git

## Environment Variables

If a module needs to have environment variables set, they should go in
`$HOME/.local/etc/profile.d/50-<module-name>`. Here `50` is the priority and
should be used as the default unless a lower or higher priority is required.

These files should adhere to the following rules, and display them at the top
of the file:

```
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
```

It is the reponsibility of the shell to load these in its config.
