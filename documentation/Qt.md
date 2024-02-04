# GUI

## Remote GUI using Qt

### ERROR
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

Aborted (core dumped)
```
Solutions
- Download `libxcb` and `xcbproto`
- Then `./configure --prefix=$HOME/.local` and `make` the `libxcb`.

You will find error

`
*** No rule to make target '//usr/local/share/xcb/', needed by 'xproto.c'.  Stop.
`

