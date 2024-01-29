from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'CTkEasyEditor')
]

setup(name='CTkEasyEditor',
      version = '1.0',
      description = 'A simple GUI editor for Custom Tkinter',
      options = {'build_exe': build_options},
      executables = executables)
