# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import PyInstaller.__main__
from pathlib import Path
from PyInstaller.building.build_main import Analysis, EXE, PYZ, COLLECT
from PyInstaller.building.api import PYZ, EXE, COLLECT, MERGE

# Get the project root directory
try:
    # First try using __file__ (works in normal Python)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = Path(script_dir).parent
except NameError:
    # If __file__ is not defined (PyInstaller context), use sys.argv[0]
    script_path = os.path.abspath(sys.argv[0])
    script_dir = os.path.dirname(script_path)
    project_root = Path(script_dir).parent

print(f"Project root: {project_root}")
print(f"Script directory: {script_dir}")
print(f"Current working directory: {os.getcwd()}")

# Set up paths
build_path = project_root / 'build'
dist_path = project_root / 'dist'
script_dir = project_root / 'script'

# Ensure paths exist
os.makedirs(build_path, exist_ok=True)
os.makedirs(dist_path, exist_ok=True)

# Main script
main_script = str(project_root / 'main.py')
if not os.path.exists(main_script):
    raise FileNotFoundError(f"Main script not found at: {main_script}")

# Analysis
a = Analysis(
    [main_script],
    pathex=[str(project_root), str(script_dir)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtNetwork',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebChannel',
        'PyQt6.QtWebSockets',
        'cryptography',
        'cryptography.hazmat.backends.openssl',
        'cryptography.hazmat.bindings._rust',
        'serial',
        'serial.tools',
        'serial.tools.list_ports',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PyZ
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MSR605',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'assets' / 'icon.ico') if (project_root / 'assets' / 'icon.ico').exists() else None,
)