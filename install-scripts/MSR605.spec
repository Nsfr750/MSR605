# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# Get the project root directory
project_root = os.path.dirname(os.path.abspath('.'))
script_dir = os.path.join(project_root, 'script')
assets_icon = os.path.join(project_root, 'assets', 'icon.ico')

# Add project root to Python path
sys.path.insert(0, project_root)

a = Analysis(
    ['main.py'],
    pathex=[project_root, script_dir],
    binaries=[],
    datas=[('assets', 'assets'), ('config', 'config'), ('script', 'script')],
    hiddenimports=['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.QtNetwork', 'PyQt6.QtWebEngineWidgets', 'PyQt6.QtWebEngineCore', 'PyQt6.QtWebChannel', 'PyQt6.QtWebSockets', 'cryptography', 'cryptography.hazmat.backends.openssl', 'cryptography.hazmat.bindings._rust', 'serial', 'serial.tools', 'serial.tools.list_ports'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MSR605',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[assets_icon] if os.path.exists(assets_icon) else None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MSR605',
)
