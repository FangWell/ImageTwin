#!/usr/bin/env python3
"""
手动依赖安装脚本 - 用于解决启动脚本安装失败的问题
"""
import subprocess
import sys
import os

def install_package(package_name, alternative_name=None):
    """安装Python包，支持备选包名"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError:
        if alternative_name:
            print(f"  Failed to install {package_name}, trying {alternative_name}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", alternative_name, "--quiet"])
                print(f"✓ {alternative_name} installed successfully")
                return True
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install both {package_name} and {alternative_name}")
                return False
        else:
            print(f"✗ Failed to install {package_name}")
            return False

def check_python_version():
    """检查Python版本兼容性"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    elif version.major == 3 and version.minor >= 12:
        print("⚠️  Using newer Python version - some packages might need compilation")
    
    return True

def main():
    print("=== 图片相似度搜索工具依赖安装器 ===\n")
    
    if not check_python_version():
        return False
    
    # 升级pip
    print("Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"])
        print("✓ pip upgraded")
    except subprocess.CalledProcessError:
        print("⚠️  pip upgrade failed, continuing...")
    
    # 定义要安装的包
    packages = [
        ("fastapi", None),
        ("uvicorn", None),
        ("python-multipart", None),
        ("Pillow", "pillow"),
        ("imagehash", None),
        ("pydantic", None),
        ("aiofiles", None)
    ]
    
    # 安装包
    failed_packages = []
    for package, alternative in packages:
        if not install_package(package, alternative):
            failed_packages.append(package)
    
    # 验证安装
    print("\n=== 验证安装 ===")
    try:
        import fastapi
        print("✓ FastAPI")
    except ImportError:
        print("✗ FastAPI")
        failed_packages.append("fastapi")
    
    try:
        import uvicorn
        print("✓ Uvicorn")
    except ImportError:
        print("✗ Uvicorn")
        failed_packages.append("uvicorn")
    
    try:
        from PIL import Image
        print("✓ Pillow")
    except ImportError:
        print("✗ Pillow")
        failed_packages.append("Pillow")
    
    try:
        import imagehash
        print("✓ ImageHash")
    except ImportError:
        print("✗ ImageHash")
        failed_packages.append("imagehash")
    
    if failed_packages:
        print(f"\n❌ 以下包安装失败: {', '.join(failed_packages)}")
        print("\n手动安装命令:")
        for pkg in failed_packages:
            print(f"  python -m pip install {pkg}")
        return False
    else:
        print("\n✅ 所有依赖包安装成功！")
        return True

if __name__ == "__main__":
    success = main()
    input("\n按回车键退出...")
    sys.exit(0 if success else 1)