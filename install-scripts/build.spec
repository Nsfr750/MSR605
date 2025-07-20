# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

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

# Debug information
print(f"[DEBUG] Script directory: {script_dir}")
print(f"[DEBUG] Project root: {project_root}")
print(f"[DEBUG] Current working directory: {os.getcwd()}")
print(f"[DEBUG] Python path: {sys.path}")

# Ensure the project root is in the Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import version from script if available
try:
    sys.path.insert(0, str(project_root))
    from script.version import __version__ as VERSION
    VERSION = VERSION
    del sys.path[0]
except ImportError:
    VERSION = '2.4.0'  # Fallback version

block_cipher = None

# Add project root to path
pathex = [str(project_root)]

# Add script and config directories if they exist
script_dir = project_root / 'script'
config_dir = project_root / 'config'
if script_dir.exists():
    pathex.append(str(script_dir))
if config_dir.exists():
    pathex.append(str(config_dir))

# Data files and assets
datas = []

# Add assets directory
assets_dir = project_root / 'assets'
if assets_dir.exists():
    datas.append((str(assets_dir / '*'), 'assets'))

# Add config directory
if config_dir.exists():
    datas.append((str(config_dir / '*'), 'config'))

# Add script directory
if script_dir.exists():
    datas.append((str(script_dir / '*.py'), 'script'))

# Add version info file
version_info = project_root / 'assets' / 'version_info.txt'
if version_info.exists():
    datas.append((str(version_info), 'assets'))

# Add other important files
for f in ['README.md', 'LICENSE', 'CHANGELOG.md', 'requirements.txt']:
    if (project_root / f).exists():
        datas.append((str(project_root / f), '.'))

# Hidden imports
hiddenimports = [
    # PyQt6 modules
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtWebEngineCore',
    'PyQt6.QtNetwork',
    'PyQt6.QtWebChannel',
    
    # Core dependencies
    'pyserial',
    'cryptography',
    'cryptography.hazmat',
    'cryptography.hazmat.primitives',
    'cryptography.hazmat.primitives.ciphers',
    'cryptography.hazmat.primitives.hashes',
    'cryptography.hazmat.primitives.kdf',
    'cryptography.hazmat.primitives.padding',
    'cryptography.hazmat.backends',
    'cryptography.hazmat.bindings',
    
    # Other dependencies
    'wand',
    'qrcode',
    'requests',
    'psutil',
    
    # Platform-specific
    *(['win32timezone', 'pywin32', 'pythoncom', 'win32com', 'win32com.shell'] if sys.platform == 'win32' else []),
    *(['AppKit', 'Foundation'] if sys.platform == 'darwin' else []),
    *(['dbus'] if sys.platform == 'linux' else [])
]

# Binaries (like DLLs, SOs)
binaries = []

# Add cryptography's Rust binary
try:
    import cryptography
    # Get the directory where cryptography is installed
    crypto_path = Path(cryptography.__file__).parent
    
    # Look for the Rust binary in multiple possible locations
    rust_binaries = []
    if sys.platform == 'win32':
        dll_name = '_rust.abi3.dll'
        # 1. Check in the cryptography package directory
        rust_binaries = list(crypto_path.glob(f'**/{dll_name}'))
        
        # 2. Check in the user's site-packages
        if not rust_binaries:
            import site
            search_paths = site.getsitepackages() + [site.getusersitepackages()]
            for path in search_paths:
                path = Path(path)
                # Check in standard location
                candidate = path / 'cryptography' / 'hazmat' / 'bindings' / dll_name
                if candidate.exists():
                    rust_binaries = [candidate]
                    break
                # Check in .libs directory (common for some installations)
                candidate = path / 'cryptography' / '.libs' / dll_name
                if candidate.exists():
                    rust_binaries = [candidate]
                    break
        
        # 3. Check in the Python installation directory
        if not rust_binaries:
            python_lib = Path(sys.base_prefix) / 'Lib' / 'site-packages'
            candidate = python_lib / 'cryptography' / 'hazmat' / 'bindings' / dll_name
            if candidate.exists():
                rust_binaries = [candidate]
    else:
        so_name = '_rust.abi3.so'
        # Similar logic for non-Windows platforms
        rust_binaries = list(crypto_path.glob(f'**/{so_name}'))
        if not rust_binaries:
            import site
            search_paths = site.getsitepackages() + [site.getusersitepackages()]
            for path in search_paths:
                path = Path(path)
                candidate = path / 'cryptography' / 'hazmat' / 'bindings' / so_name
                if candidate.exists():
                    rust_binaries = [candidate]
                    break
                # Check in .libs directory
                candidate = path / 'cryptography' / '.libs' / so_name
                if candidate.exists():
                    rust_binaries = [candidate]
                    break
    
    # Add all found Rust binaries
    for rust_bin in rust_binaries:
        print(f"Found cryptography Rust binary at: {rust_bin}")
        binaries.append((str(rust_bin), 'cryptography/hazmat/bindings/'))
except Exception as e:
    print(f"Warning: Could not find cryptography Rust binary: {e}")
    print("The application may not work correctly without it.")
    print("Try installing cryptography with: pip install --upgrade cryptography")

# Ensure main.py path is correct
main_script = str(project_root / 'main.py')
print(f"[DEBUG] Main script path: {main_script}")

if not os.path.exists(main_script):
    raise FileNotFoundError(f"Main script not found at: {main_script}")

a = Analysis(
    [main_script],
    pathex=pathex,
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'pillow',
        'PIL',
        'unittest',
        'email',
        'http',
        'xml',
        'pydoc',
        'pdb',
        'doctest',
        'test',
        'tests',
        'setuptools',
        'pip',
        'wheel',
        'distutils',
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
        'notebook',
        'jupyter',
        'IPython',
        'PySide2',
        'PySide6',
        'PyQt5',
        'PyQt6.QtWebEngineWidgets' if sys.platform != 'win32' else ''
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Windows specific options
if sys.platform == 'win32':
    # Use the icon from assets if it exists
    icon_path = str(assets_dir / 'icon.ico')
    if not os.path.exists(icon_path):
        icon_path = None
    
    # Version info file path
    version_info_path = str(version_info) if version_info.exists() else None
    
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='MSR605',
        debug=False,
        bootloader_ignore_signals=True,
        strip=True,
        upx=True,
        upx_exclude=[
            "cryptography-*.so",
            "_cffi_backend.*",
            "_cffi_*.*",
            "_cffi_*",
            "_cffi_backend"
        ],
        runtime_tmpdir='.',
        console=False,  # No console window for the application
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_path,
        version=version_info_path,
        uac_admin=False,
        uac_uiaccess=False,
        onefile=True,
    )
else:
    # Non-Windows platforms
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='MSR605',
        debug=False,
        bootloader_ignore_signals=True,
        strip=True,
        upx=True,
        upx_exclude=[
            "cryptography-*.so",
            "_cffi_backend.*",
            "_cffi_*.*",
            "_cffi_*",
            "_cffi_backend"
        ],
        runtime_tmpdir='.',
        console=False,  # No console window for the application
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,
        version=None,
        uac_admin=False,
        uac_uiaccess=False,
        onefile=True,
    )
