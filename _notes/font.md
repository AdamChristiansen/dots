# Fonts

Use the following to install a font for a single user:

```sh
# This is where user installed fonts live
mkdir ~/.local/share/fonts
# Copy the fonts over
mv FONTNAME-Regular.ttf    ~/.local/share/fonts/FONTNAME-Regular.ttf
mv FONTNAME-Italic.ttf     ~/.local/share/fonts/FONTNAME-Italic.ttf
mv FONTNAME-Bold.ttf       ~/.local/share/fonts/FONTNAME-Bold.ttf
mv FONTNAME-BoldItalic.ttf ~/.local/share/fonts/FONTNAME-BoldItalic.ttf
# Regenerate the font cache
fc-cache -fv
# Check that the font is installed
fc-list | grep FONTNAME
```
