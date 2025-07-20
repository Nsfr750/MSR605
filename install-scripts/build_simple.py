#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple build script for MSR605 Card Reader/Writer Windows installer.
"""
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path


def clean_directory(dir_path):
    """Remove directory if it exists and recreate it."""
    if dir_path.exists():
        shutil.rmtree(dir_path, ignore_errors=True)
    dir_path.mkdir(parents=True, exist_ok=True)


def run_command(cmd, cwd=None):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.output


def create_portable_archive():
    """Create a portable archive of the built application."""
    print("\n" + "=" * 80)
    print("📦 Creating portable archive")
    print("=" * 80)

    import zipfile
    from datetime import datetime

    base_dir = Path(__file__).parent.parent  # Go up one level to project root
    dist_dir = base_dir / "dist"
    exe_path = dist_dir / "MSR605.exe"

    if not exe_path.exists():
        print("❌ Executable not found. Please build the application first.")
        return False

    # Create a version string for the archive name
    try:
        from script.version import __version__

        version_str = __version__
    except ImportError:
        version_str = datetime.now().strftime("%Y%m%d")

    archive_name = f"MSR605-Card-Reader-Writer-v{version_str}.zip"
    archive_path = dist_dir / archive_name

    print(f"📁 Creating archive: {archive_path}")

    try:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add the executable
            zipf.write(exe_path, arcname=exe_path.name)

            # Add necessary directories
            dirs_to_include = ["assets", "config", "script", "Docs"]

            for dir_name in dirs_to_include:
                src_dir = base_dir / dir_name
                if src_dir.exists():
                    for root, _, files in os.walk(src_dir):
                        for file in files:
                            # Skip Python cache and temporary files
                            if any(
                                part.startswith("__pycache__") or part.endswith(".pyc")
                                for part in Path(root).parts
                            ):
                                continue

                            file_path = Path(root) / file
                            arcname = file_path.relative_to(base_dir)
                            zipf.write(file_path, arcname=arcname)

            # Add a README.txt
            readme_content = """MSR605 Card Reader/Writer - Portable Version

This is a portable version of the MSR605 Card Reader/Writer application. 
Simply extract this archive and run MSR605.exe.

Version: {}
Build date: {}
""".format(
                version_str, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            zipf.writestr("README.txt", readme_content)

        print(f"✅ Successfully created portable archive: {archive_path}")
        print(f"   Archive size: {archive_path.stat().st_size / 1024 / 1024:.2f} MB")
        return True
    except Exception as e:
        print(f"❌ Failed to create portable archive: {e}")
        if archive_path.exists():
            archive_path.unlink()
        return False


def build_installer():
    """Build the Windows installer using PyInstaller with the spec file."""
    print("\n" + "=" * 80)
    print("🚀 Building MSR605 Card Reader/Writer")
    print("=" * 80)

    # Clean build directories
    print("🧹 Cleaning build directories...")
    build_dir = Path(__file__).parent.parent / "build"
    dist_dir = Path(__file__).parent.parent / "dist"
    clean_directory(build_dir)
    clean_directory(dist_dir)

    # Get Python executable path
    python_exe = sys.executable
    print(f"🐍 Using Python executable: {python_exe}")

    # Get project root directory and spec file path
    project_root = Path(__file__).parent.parent
    spec_file = Path(__file__).parent / "build.spec"
    print(f"📁 Project root: {project_root}")
    print(f"📝 Using spec file: {spec_file}")

    # Build the PyInstaller command using the spec file
    pyinstaller_cmd = [
        python_exe,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",  # Don't ask for confirmation when overwriting
        f"--distpath={project_root / 'dist'}",
        f"--workpath={project_root / 'build'}",
        str(spec_file),
    ]

    # Run PyInstaller with full output capture
    print("\n🔨 Running PyInstaller command:")
    cmd_str = " ".join(
        f'"{arg}"' if " " in str(arg) else str(arg) for arg in pyinstaller_cmd
    )
    print(cmd_str)
    print("\n📝 PyInstaller output:")
    print("-" * 80)

    # Create build directory if it doesn't exist
    (project_root / "build").mkdir(exist_ok=True)
    build_log = project_root / "build" / "build.log"

    # Run the command and capture output
    try:
        # First, try to find the exact location of the cryptography Rust binary
        print("\n🔍 Checking for cryptography Rust binary...")
        try:
            import cryptography

            crypto_path = Path(cryptography.__file__).parent
            print(f"Cryptography path: {crypto_path}")

            # Look for the Rust binary in multiple locations
            rust_binaries = []
            if sys.platform == "win32":
                rust_binaries = list(crypto_path.glob("**/_rust.abi3.dll"))
                print(
                    f"Found {len(rust_binaries)} Rust binaries in cryptography package"
                )

                # Also check site-packages
                if not rust_binaries:
                    import site

                    for path in site.getsitepackages() + [site.getusersitepackages()]:
                        search_path = (
                            Path(path)
                            / "cryptography"
                            / "hazmat"
                            / "bindings"
                            / "_rust.abi3.dll"
                        )
                        print(f"Checking {search_path}")
                        if search_path.exists():
                            rust_binaries = [search_path]
                            print(f"Found Rust binary at: {search_path}")
                            break

            if rust_binaries:
                print(f"✅ Found cryptography Rust binary at: {rust_binaries[0]}")
            else:
                print("⚠️ Could not find cryptography Rust binary. The build may fail.")
                print("Try running: pip install --upgrade cryptography")

        except Exception as e:
            print(f"⚠️ Error checking for cryptography: {e}")

        # Run PyInstaller
        print("\n🚀 Starting PyInstaller build...")
        process = subprocess.Popen(
            pyinstaller_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=project_root,
            shell=True,  # Use shell to ensure proper command execution
        )

        # Print and capture output in real-time
        output_lines = []
        for line in process.stdout:
            print(line, end="")
            output_lines.append(line)

        process.wait()
        success = process.returncode == 0
        output = "".join(output_lines)

        # Save full output to log file
        with open(build_log, "w", encoding="utf-8") as f:
            f.write(output)

        if success:
            print("\n✅ Build completed successfully!")
            print(f"📦 Output directory: {project_root / 'dist'}")
        else:
            print(f"\n❌ Build failed with exit code {process.returncode}")
            print(f"📄 Full build output saved to: {build_log}")

            # Print the last 20 lines of the log for quick reference
            print("\n📋 Last 20 lines of build output:")
            print("-" * 80)
            print("\n".join(output_lines[-20:]))

        return success

    except Exception as e:
        error_msg = f"Error running PyInstaller: {str(e)}"
        print(f"\n❌ {error_msg}")
        with open(build_log, "a", encoding="utf-8") as f:
            f.write(f"\n\nFATAL ERROR: {error_msg}")
        print(f"\n📄 Error details saved to: {build_log}")
        return False

    return success

    print("\n" + "-" * 80)

    # Check if build was successful
    exe_path = dist_dir / "MSR605.exe"
    if return_code == 0 and exe_path.exists():
        print(f"\n✅ Successfully built: {exe_path}")
        print(f"   File size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")

        # Create portable archive after successful build
        create_portable_archive()

        return True
    else:
        print("\n❌ Build failed")
        print(f"   Return code: {return_code}")
        print(f"   Executable exists: {exe_path.exists()}")

        # Save the full output to a file for debugging
        log_file = base_dir / "build_failure.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n📄 Full build output saved to: {log_file}")

        return False


if __name__ == "__main__":
    build_installer()
