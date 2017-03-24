
Debian
====================
This directory contains files used to package smartcashd/smartcash-qt
for Debian-based Linux systems. If you compile smartcashd/smartcash-qt yourself, there are some useful files here.

## smartcash: URI support ##


smartcash-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install smartcash-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your smartcash-qt binary to `/usr/bin`
and the `../../share/pixmaps/smartcash128.png` to `/usr/share/pixmaps`

smartcash-qt.protocol (KDE)

