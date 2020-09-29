# Initialize features for non-reparenting WMs.

# The standard Java GUI tookit keeps a list of known non-reparenting window
# managers. If using one that is not on that list, the windows might display a
# blank screen. This can be solved by explicitly setting that the window
# manager is non-reparenting.
export _JAVA_AWT_WM_NONREPARENTING=1
