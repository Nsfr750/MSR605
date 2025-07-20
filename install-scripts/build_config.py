"""
Build configuration for MSR605 Card Reader/Writer platform-specific installers.
"""

from pathlib import Path
import sys
import platform
from script.version import __version__ as VERSION

# Project information
PROJECT_NAME = "MSR605"
VERSION = VERSION
AUTHOR = "Nsfr750"
DESCRIPTION = "A tool for reading from and writing to magnetic stripe cards using the MSR605 device."
COPYRIGHT = f"(c) 2025 {AUTHOR}"

# Try to get version from script if available
try:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from script.version import __version__ as VERSION

    VERSION = VERSION
    del sys.path[0]
except ImportError:
    pass

# Paths
ROOT_DIR = Path(__file__).parent.parent  # Project root
ASSETS_DIR = ROOT_DIR / "assets"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
SCRIPT_DIR = ROOT_DIR / "script"
CONFIG_DIR = ROOT_DIR / "config"
DOCS_DIR = ROOT_DIR / "Docs"

# Platform-specific configurations
PLATFORMS = {
    "Windows": {
        "name": "Windows",
        "executable": f"{PROJECT_NAME}.exe",
        "installer": {
            "type": "nsis",
            "extension": "exe",
            "extra_args": [
                "--windowed",
                "--onefile",
                "--noconsole",
                "--name",
                f"{PROJECT_NAME}-{VERSION}-Windows",
                "--icon",
                str(ASSETS_DIR / "icon.ico"),
                "--add-binary",
                f"{sys.base_prefix}/Lib/site-packages/cryptography/hazmat/bindings/_rust.abi3.dll;cryptography/hazmat/bindings/",
            ],
            "nsis": {
                "install_icon": str(ASSETS_DIR / "icon.ico"),
                "uninstall_icon": str(ASSETS_DIR / "icon.ico"),
                "header_image": (
                    str(ASSETS_DIR / "nsis-header.bmp")
                    if (ASSETS_DIR / "nsis-header.bmp").exists()
                    else None
                ),
                "wizard_image": (
                    str(ASSETS_DIR / "nsis-wizard.bmp")
                    if (ASSETS_DIR / "nsis-wizard.bmp").exists()
                    else None
                ),
                "sidebar_image": (
                    str(ASSETS_DIR / "nsis-sidebar.bmp")
                    if (ASSETS_DIR / "nsis-sidebar.bmp").exists()
                    else None
                ),
                "installer_name": f"{PROJECT_NAME}-{VERSION}-Setup",
                "install_directory": "$PROGRAMFILES\\MSR605",
                "menu_prompt": "Start Menu Folder",
                "create_desktop_icon": True,
                "create_start_menu_shortcut": True,
                "uninstall_name": "Uninstall MSR605",
            },
        },
        "archive": {
            "formats": ["zip"],
            "include": [
                f"{PROJECT_NAME}.exe",
                "assets/*",
                "config/*",
                "script/*",
                "LICENSE",
                "README.md",
                "requirements.txt",
            ],
        },
    },
    "Darwin": {
        "name": "macOS",
        "executable": f"{PROJECT_NAME}.app",
        "installer": {
            "type": "dmg",
            "extension": "dmg",
            "extra_args": [
                "--windowed",
                "--osx-bundle-identifier",
                f"com.{AUTHOR.lower()}.{PROJECT_NAME.lower()}",
                "--icon",
                (
                    str(ASSETS_DIR / "icon.icns")
                    if (ASSETS_DIR / "icon.icns").exists()
                    else None
                ),
                "--name",
                f"{PROJECT_NAME}-{VERSION}-macOS",
                "--osx-entitlements-file",
                (
                    str(ASSETS_DIR / "entitlements.plist")
                    if (ASSETS_DIR / "entitlements.plist").exists()
                    else None
                ),
                "--add-binary",
                f"{sys.base_prefix}/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages/cryptography/hazmat/bindings/_rust.abi3.so;cryptography/hazmat/bindings/",
            ],
            "dmg": {
                "volume_name": f"{PROJECT_NAME} {VERSION}",
                "background": (
                    str(ASSETS_DIR / "dmg-background.png")
                    if (ASSETS_DIR / "dmg-background.png").exists()
                    else None
                ),
                "icon_size": 80,
                "text_size": 12,
                "window_rect": {"x": 100, "y": 100, "width": 500, "height": 300},
            },
        },
        "archive": {
            "formats": ["zip"],
            "include": [
                f"{PROJECT_NAME}.app",
                "LICENSE",
                "README.md",
                "requirements.txt",
            ],
        },
    },
    "Linux": {
        "name": "Linux",
        "executable": PROJECT_NAME,
        "installer": {
            "type": "appimage",
            "extension": "AppImage",
            "extra_args": [
                "--windowed",
                "--name",
                f"{PROJECT_NAME}-{VERSION}-Linux",
                "--icon",
                (
                    str(ASSETS_DIR / "icon.png")
                    if (ASSETS_DIR / "icon.png").exists()
                    else None
                ),
                "--runtime-tmpdir",
                "/tmp",
                "--add-binary",
                f"{sys.base_prefix}/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages/cryptography/hazmat/bindings/_rust.abi3.so;cryptography/hazmat/bindings/",
            ],
            "appimage": {
                "update-information": None,
                "sign": False,  # Disable signing by default as it requires additional setup
                "sign-args": ["--sign"],
                "runtime-file": "appruntime",
            },
        },
        "archive": {
            "formats": ["tar.gz", "zip"],
            "include": [
                f"{PROJECT_NAME}-{VERSION}-Linux.AppImage",
                f"{PROJECT_NAME}.desktop",
                "LICENSE",
                "README.md",
                "requirements.txt",
            ],
        },
        "deb": {
            "enabled": True,
            "dependencies": [
                "python3",
                "python3-pip",
                "python3-pyqt6",
                "python3-serial",
                "python3-cryptography",
                "python3-wand",
                "python3-requests",
                "python3-psutil",
            ],
            "maintainer": f"{AUTHOR} <nsfr750@yandex.com>",
            "section": "utils",
            "architecture": "amd64",
            "description": DESCRIPTION,
            "pre_install_script": (
                "preinst" if (ROOT_DIR / "debian/preinst").exists() else None
            ),
            "post_install_script": (
                "postinst" if (ROOT_DIR / "debian/postinst").exists() else None
            ),
            "pre_uninstall_script": (
                "prerm" if (ROOT_DIR / "debian/prerm").exists() else None
            ),
            "post_uninstall_script": (
                "postrm" if (ROOT_DIR / "debian/postrm").exists() else None
            ),
        },
    },
}

# Common PyInstaller configurations
PYINSTALLER_CONFIG = {
    "hidden_imports": [
        # PyQt6 modules
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "PyQt6.QtWebEngineWidgets",
        "PyQt6.QtWebEngineCore",
        "PyQt6.QtNetwork",
        "PyQt6.QtWebChannel",
        # Core dependencies
        "pyserial",
        "cryptography",
        "cryptography.hazmat",
        "cryptography.hazmat.primitives",
        "cryptography.hazmat.primitives.ciphers",
        "cryptography.hazmat.primitives.hashes",
        "cryptography.hazmat.primitives.kdf",
        "cryptography.hazmat.primitives.padding",
        "cryptography.hazmat.backends",
        "cryptography.hazmat.bindings",
        "wand",
        "qrcode",
        "requests",
        "psutil",
        # Platform-specific
        *(
            ["win32timezone", "pywin32", "pythoncom", "win32com", "win32com.shell"]
            if sys.platform == "win32"
            else []
        ),
        *(["AppKit", "Foundation"] if sys.platform == "darwin" else []),
        *(["dbus"] if sys.platform == "linux" else []),
    ],
    "data_files": [
        (str(ASSETS_DIR), "assets"),
        (str(CONFIG_DIR), "config") if CONFIG_DIR.exists() else None,
        (str(SCRIPT_DIR), "script") if SCRIPT_DIR.exists() else None,
        (str(DOCS_DIR), "Docs") if DOCS_DIR.exists() else None,
        (
            (str(ROOT_DIR / "README.md"), ".")
            if (ROOT_DIR / "README.md").exists()
            else None
        ),
        (str(ROOT_DIR / "LICENSE"), ".") if (ROOT_DIR / "LICENSE").exists() else None,
        (
            (str(ROOT_DIR / "CHANGELOG.md"), ".")
            if (ROOT_DIR / "CHANGELOG.md").exists()
            else None
        ),
        (
            (str(ROOT_DIR / "requirements.txt"), ".")
            if (ROOT_DIR / "requirements.txt").exists()
            else None
        ),
    ],
    "binaries": [
        # Include cryptography's Rust binary
        (
            (
                str(
                    Path(sys.base_prefix)
                    / f"Lib/site-packages/cryptography/hazmat/bindings/_rust.abi3.dll"
                ),
                "cryptography/hazmat/bindings/",
            )
            if sys.platform == "win32"
            else None
        ),
        (
            (
                str(
                    Path(sys.base_prefix)
                    / f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages/cryptography/hazmat/bindings/_rust.abi3.so"
                ),
                "cryptography/hazmat/bindings/",
            )
            if sys.platform in ["linux", "darwin"]
            else None
        ),
    ],
    "excludes": [
        "tkinter",
        "pillow",
        "PIL",
        "unittest",
        "email",
        "http",
        "xml",
        "pydoc",
        "pdb",
        "doctest",
        "test",
        "tests",
        "setuptools",
        "pip",
        "wheel",
        "distutils",
        "numpy",  # Only include if explicitly needed
        "scipy",
        "matplotlib",
        "pandas",
        "notebook",
        "jupyter",
        "IPython",
        "PySide2",
        "PySide6",
        "PyQt5",
        (
            "PyQt6.QtWebEngineWidgets"
            if not PLATFORMS.get(platform.system(), {}).get("installer", {}).get("type")
            == "nsis"
            else ""
        ),
    ],
    "upx": True,
    "upx_exclude": [
        # Add any files that should be excluded from UPX compression
        "cryptography-*.so",
        "_cffi_backend.*",
        "_cffi_*.*",
        "_cffi_*",
        "_cffi_backend",
    ],
    "no_compress": False,
    "optimize": 1,
    "strip": True,
    "console": False,
    "debug": False,
    "runtime_tmpdir": ".",
    "pathex": [
        str(ROOT_DIR),
        str(SCRIPT_DIR) if SCRIPT_DIR.exists() else None,
        str(CONFIG_DIR) if CONFIG_DIR.exists() else None,
    ],
}
