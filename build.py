# -*- coding: utf-8 -*-
"""Build the Elephas UCI engine into an executable file using PyInstaller."""

import PyInstaller.__main__

PyInstaller.__main__.run([
    'uci.py',
    '--onefile',
    '--name', 'elephas'
])
