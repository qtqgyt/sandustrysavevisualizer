import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '-F',
    '-n',
    'Sandustry Save Viewer/Editor',
    '--disable-windowed-traceback'
])