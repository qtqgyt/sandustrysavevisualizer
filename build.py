import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '-F',
    '-n',
    'Sandustry Save Viewer and Editor',
    '--disable-windowed-traceback',
    '-i',
    'image.ico'
])