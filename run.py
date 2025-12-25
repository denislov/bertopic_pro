#!/usr/bin/env python
"""
BERTopic Pro - 灵活启动脚本
自动检测环境并选择最佳启动方式
"""

import sys
import os
import subprocess


def check_display():
    """检查是否有可用的显示环境"""
    return os.environ.get('DISPLAY') is not None


def check_xvfb():
    """检查是否安装了 Xvfb"""
    try:
        subprocess.run(['which', 'Xvfb'],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except:
        return False


def run_with_display():
    """在有显示环境中运行"""
    print("✓ 检测到显示环境，正常启动...")
    os.execvp(sys.executable, [sys.executable, 'main.py'])


def run_with_xvfb():
    """使用 Xvfb 虚拟显示运行"""
    print("✓ 使用 Xvfb 虚拟显示启动...")
    print("  (应用在后台运行，不会显示窗口)")
    os.execvp('xvfb-run', ['xvfb-run', '-a', sys.executable, 'main.py'])


def run_offscreen():
    """使用 offscreen 插件运行（仅测试）"""
    print("⚠️  无显示环境，使用 offscreen 模式（仅用于测试）")
    print("  (应用不会显示窗口)")
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    os.execvp(sys.executable, [sys.executable, 'main.py'])


def show_install_instructions():
    """显示安装说明"""
    print("\n" + "=" * 60)
    print("💡 如何在服务器上运行 GUI 应用？")
    print("=" * 60)
    print("\n方案 1: 安装 Xvfb（虚拟显示）")
    print("  Ubuntu/Debian:")
    print("    sudo apt-get install xvfb")
    print("  然后重新运行此脚本\n")

    print("方案 2: 使用 VNC 或远程桌面")
    print("  1. 安装 VNC 服务器")
    print("  2. 通过 VNC 客户端连接")
    print("  3. 在远程桌面中运行应用\n")

    print("方案 3: 在本地开发机器上运行")
    print("  1. 将代码复制到有显示器的机器")
    print("  2. 安装依赖: pip install -e .")
    print("  3. 运行: python main.py\n")

    print("方案 4: 仅运行架构测试（无 GUI）")
    print("  python test_architecture.py")
    print("=" * 60)


def main():
    print("\n🚀 BERTopic Pro 启动器")
    print("=" * 60)

    # 检查显示环境
    has_display = check_display()
    has_xvfb = check_xvfb()

    if has_display:
        # 有显示环境，正常启动
        run_with_display()
    elif has_xvfb:
        # 无显示但有 Xvfb，使用虚拟显示
        run_with_xvfb()
    else:
        # 都没有，显示说明
        print("\n⚠️  无法检测到图形显示环境")
        print(f"  - DISPLAY 环境变量: {os.environ.get('DISPLAY', '(未设置)')}")
        print(f"  - Xvfb 可用: 否")

        print("\n选项：")
        print("  1. 运行架构测试（无 GUI）")
        print("  2. 强制使用 offscreen 模式")
        print("  3. 查看安装说明")
        print("  4. 退出")

        choice = input("\n请选择 (1-4): ").strip()

        if choice == '1':
            print("\n启动架构测试...")
            os.execvp(sys.executable, [sys.executable, 'test_architecture.py'])
        elif choice == '2':
            run_offscreen()
        elif choice == '3':
            show_install_instructions()
        else:
            print("退出")
            sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n中断退出")
        sys.exit(0)
