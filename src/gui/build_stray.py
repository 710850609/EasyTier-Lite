#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller Build Script - System Tray App
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Set UTF-8 encoding (Windows compatible)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
GUI_DIR = Path(__file__).parent.absolute()
BUILD_DIR = GUI_DIR / "build"
DIST_DIR = GUI_DIR / "dist"

def run_command(cmd, cwd=None):
    """Execute command and return result"""
    print(f"Execute: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or str(GUI_DIR),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        if result.stdout:
            print(result.stdout)
        return True
    except Exception as e:
        print(f"Command failed: {e}")
        return False

def install_deps():
    """Install dependencies"""
    print("[1/4] Installing dependencies...")
    deps = ["pyinstaller", "pystray", "pillow"]
    mirror = "-i https://pypi.tuna.tsinghua.edu.cn/simple"
    
    # Check if in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # Use --break-system-packages if not in venv
    if not in_venv:
        break_system = "--break-system-packages"
        print(f"  System Python detected, using {break_system}")
    else:
        break_system = ""
        print("  Virtual environment detected")
    
    return run_command(f"pip install {' '.join(deps)} {mirror} {break_system}")

def get_platform_name():
    """Get platform name (auto-detect architecture)"""
    import platform
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Architecture mapping
    arch_map = {
        'x86_64': 'x64',
        'amd64': 'x64',
        'i386': 'x86',
        'i686': 'x86',
        'aarch64': 'arm64',
        'arm64': 'arm64',
        'armv7l': 'arm',
        'armv6l': 'arm',
    }
    
    arch = arch_map.get(machine, machine)
    
    if system == "windows":
        return f"windows-{arch}"
    elif system == "linux":
        return f"linux-{arch}"
    elif system == "darwin":
        return f"macos-{arch}"
    return f"{system}-{arch}"

def build_executable():
    """Build executable"""
    print("[2/4] Building...")
    
    platform_name = get_platform_name()
    output_name = f"EasyTierLite-Tray-{platform_name}"
    
    # Icon path
    icon_path = GUI_DIR / "icon.png"
    if not icon_path.exists():
        icon_path = PROJECT_ROOT / "frontend" / "icon.png"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", output_name,
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(GUI_DIR),
        "--hidden-import", "pystray._win32" if sys.platform == "win32" else "pystray._appindicator",
        "--hidden-import", "PIL._tkinter_finder",
    ]
    
    # Add icon (Windows uses .ico, others use .png)
    if icon_path.exists():
        if sys.platform == "win32":
            # Windows prefers .ico format
            ico_path = GUI_DIR / "icon.ico"
            if not ico_path.exists():
                print(f"  Warning: Windows prefers .ico icon")
            else:
                cmd.extend(["--icon", str(ico_path)])
        cmd.extend(["--add-data", f"{icon_path}{os.pathsep}."])
    
    # Windows specific options
    if sys.platform == "win32":
        cmd.extend(["--console"])
    
    cmd.append(str(GUI_DIR / "stray.py"))
    
    result = run_command(" ".join(cmd))
    return result, output_name

def copy_output(output_name):
    """Copy output file"""
    print("[3/4] Copying output...")
    
    ext = ".exe" if sys.platform == "win32" else ""
    source = DIST_DIR / f"{output_name}{ext}"
    
    output_dir = PROJECT_ROOT / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if source.exists():
        target = output_dir / f"{output_name}{ext}"
        shutil.copy2(source, target)
        print(f"  Copied to: {target}")
        return True
    else:
        print(f"  Not found: {source}")
        return False

def clean():
    """Clean build files"""
    print("[4/4] Cleaning...")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    spec_file = GUI_DIR / f"EasyTierLite-Tray-*.spec"
    import glob
    for f in glob.glob(str(spec_file)):
        os.remove(f)
    print("  Clean complete")

def main():
    print("=" * 50)
    print("EasyTierLite Tray Builder")
    print("=" * 50)
    
    # Clean old files
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    if not install_deps():
        print("[Error] Failed to install dependencies")
        sys.exit(1)
    
    result, output_name = build_executable()
    if not result:
        print("[Error] Build failed")
        sys.exit(1)
    
    if not copy_output(output_name):
        print("[Error] Failed to copy output")
        sys.exit(1)
    
    clean()
    
    print("=" * 50)
    print("Build complete!")
    print(f"Output: dist/{output_name}")
    print("=" * 50)

if __name__ == "__main__":
    main()
