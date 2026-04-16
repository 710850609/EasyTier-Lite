#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包脚本 - 系统托盘程序
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
GUI_DIR = Path(__file__).parent.absolute()
BUILD_DIR = GUI_DIR / "build"
DIST_DIR = GUI_DIR / "dist"

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    print(f"执行: {cmd}")
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
            print(f"错误: {result.stderr}")
            return False
        if result.stdout:
            print(result.stdout)
        return True
    except Exception as e:
        print(f"命令执行失败: {e}")
        return False

def install_deps():
    """安装依赖"""
    print("[1/4] 安装依赖...")
    deps = ["pyinstaller", "pystray", "pillow"]
    mirror = "-i https://pypi.tuna.tsinghua.edu.cn/simple"
    
    # 检测是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    # 如果不在虚拟环境中，使用 --break-system-packages
    if not in_venv:
        break_system = "--break-system-packages"
        print(f"  检测到系统 Python，使用 {break_system}")
    else:
        break_system = ""
        print("  检测到虚拟环境")
    
    return run_command(f"pip install {' '.join(deps)} {mirror} {break_system}")

def get_platform_name():
    """获取平台名称（自动检测架构）"""
    import platform
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # 架构映射
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
    """构建可执行文件"""
    print("[2/4] 开始打包...")
    
    platform_name = get_platform_name()
    output_name = f"EasyTierLite-Tray-{platform_name}"
    
    # 图标路径
    icon_path = GUI_DIR / "icon.png"
    if not icon_path.exists():
        icon_path = PROJECT_ROOT / "frontend" / "icon.png"
    
    # PyInstaller 命令
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
    
    # 添加图标（Windows 使用 .ico，其他平台使用 .png）
    if icon_path.exists():
        if sys.platform == "win32":
            # Windows 需要 .ico 格式
            ico_path = GUI_DIR / "icon.ico"
            if not ico_path.exists():
                print(f"  警告: Windows 建议使用 .ico 图标")
            else:
                cmd.extend(["--icon", str(ico_path)])
        cmd.extend(["--add-data", f"{icon_path}{os.pathsep}."])
    
    # Windows 特定选项
    if sys.platform == "win32":
        cmd.extend(["--console"])
    
    cmd.append(str(GUI_DIR / "stray.py"))
    
    result = run_command(" ".join(cmd))
    return result, output_name

def copy_output(output_name):
    """复制输出文件"""
    print("[3/4] 复制输出文件...")
    
    ext = ".exe" if sys.platform == "win32" else ""
    source = DIST_DIR / f"{output_name}{ext}"
    
    output_dir = PROJECT_ROOT / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if source.exists():
        target = output_dir / f"{output_name}{ext}"
        shutil.copy2(source, target)
        print(f"  复制到: {target}")
        return True
    else:
        print(f"  未找到: {source}")
        return False

def clean():
    """清理构建文件"""
    print("[4/4] 清理...")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    spec_file = GUI_DIR / f"EasyTierLite-Tray-*.spec"
    import glob
    for f in glob.glob(str(spec_file)):
        os.remove(f)
    print("  清理完成")

def main():
    print("=" * 50)
    print("EasyTierLite Tray 打包工具")
    print("=" * 50)
    
    # 清理旧文件
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    if not install_deps():
        print("[错误] 安装依赖失败")
        sys.exit(1)
    
    result, output_name = build_executable()
    if not result:
        print("[错误] 打包失败")
        sys.exit(1)
    
    if not copy_output(output_name):
        print("[错误] 复制文件失败")
        sys.exit(1)
    
    clean()
    
    print("=" * 50)
    print("打包完成!")
    print(f"输出: dist/{output_name}")
    print("=" * 50)

if __name__ == "__main__":
    main()
