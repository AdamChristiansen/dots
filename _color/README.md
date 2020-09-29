# Color Themes

Color themes are defined using the
[`base16`](https://github.com/chriskempson/base16) guidelines, which are

- `base00`: Default Background
- `base01`: Lighter Background (Used for status bars)
- `base02`: Selection Background
- `base03`: Comments, Invisibles, Line Highlighting
- `base04`: Dark Foreground (Used for status bars)
- `base05`: Default Foreground, Caret, Delimiters, Operators
- `base06`: Light Foreground (Not often used)
- `base07`: Light Background (Not often used)
- `base08`: Variables, XML Tags, Markup Link Text, Markup Lists, Diff Deleted
- `base09`: Integers, Boolean, Constants, XML Attributes, Markup Link Url
- `base0A`: Classes, Markup Bold, Search Text Background
- `base0B`: Strings, Inherited Class, Markup Code, Diff Inserted
- `base0C`: Support, Regular Expressions, Escape Characters, Markup Quotes
- `base0D`: Functions, Methods, Attribute IDs, Headings
- `base0E`: Keywords, Storage, Selector, Markup Italic, Diff Changed
- `base0F`: Deprecated, Opening/Closing Embedded Language Tags

In addition, the `base16` colors are treated in following way:

- `base00` to `base07`: Same as above
- `base08`: Red
- `base09`: Orange
- `base0A`: Yellow
- `base0B`: Green
- `base0C`: Cyan
- `base0D`: Blue
- `base0E`: Pink
- `base0F`: Purple

It is not necessary for `base08` to be specified as red, however, it will be
used with _red semantics_.

The following should be defined in a JSON file for each scheme:

* `color_base00_hex`
* `color_base01_hex`
* `color_base02_hex`
* `color_base03_hex`
* `color_base04_hex`
* `color_base05_hex`
* `color_base06_hex`
* `color_base07_hex`
* `color_base08_hex`
* `color_base09_hex`
* `color_base0A_hex`
* `color_base0B_hex`
* `color_base0C_hex`
* `color_base0D_hex`
* `color_base0E_hex`
* `color_base0F_hex`
* `color_theme`: can be `dark` or `light`
* `color_wall_hex`

where all colors are RGB hex values without the leading `#`.
