# BERTopic Pro 运行指南

## 问题诊断

您遇到的错误 `Could not load the Qt platform plugin "xcb"` 是因为：

1. **缺少 X11 库**: 系统缺少 `xcb-cursor0` 等 Qt 需要的库
2. **无图形环境**: 当前环境没有 X11 显示服务器（无头服务器）

## ✅ 已验证：架构完全正常

运行架构测试证明代码完全正常：
```bash
python test_architecture.py
```

结果：✅ **所有测试通过！**

## 🚀 运行方案

### 方案 A: 灵活启动脚本（推荐）

使用智能启动脚本，自动选择最佳方式：

```bash
python run.py
```

启动脚本会：
- 自动检测显示环境
- 如果有 Xvfb 则使用虚拟显示
- 否则提供选项菜单

### 方案 B: 在本地开发机器运行（最佳体验）

**适用于**: Windows/macOS/Linux 桌面环境

1. 复制代码到本地机器
2. 安装依赖:
   ```bash
   pip install -e .
   ```
3. 直接运行:
   ```bash
   python main.py
   ```

### 方案 C: 安装 Xvfb（服务器虚拟显示）

**适用于**: 需要在服务器运行 GUI 测试

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y xvfb

# 使用 Xvfb 运行
xvfb-run -a python main.py
```

### 方案 D: 安装缺失的库（如果有 X11）

**适用于**: 有 X11 服务器但缺少库

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-shape0

python main.py
```

### 方案 E: VNC 远程桌面

**适用于**: 需要远程访问 GUI

1. 安装 VNC 服务器:
   ```bash
   sudo apt-get install tigervnc-standalone-server
   vncserver :1
   ```

2. 通过 VNC 客户端连接

3. 在 VNC 桌面中运行:
   ```bash
   export DISPLAY=:1
   python main.py
   ```

### 方案 F: Offscreen 模式（仅测试）

**适用于**: 仅验证架构，不需要显示

```bash
export QT_QPA_PLATFORM=offscreen
python main.py
```

⚠️ 注意：此模式下看不到窗口，仅用于测试

## 📝 快速命令参考

```bash
# 架构测试（无需 GUI）
python test_architecture.py

# 智能启动
python run.py

# 直接启动（需要显示环境）
python main.py

# Xvfb 虚拟显示
xvfb-run -a python main.py

# Offscreen 测试模式
QT_QPA_PLATFORM=offscreen python main.py
```

## 🐛 常见问题

### Q: 为什么无法显示窗口？
A: 当前环境是无头服务器（没有显示器）。使用方案 B（本地运行）或方案 C（Xvfb）。

### Q: DeprecationWarning 是什么？
A: 这是 Qt 6.5+ 的 API 废弃警告，已修复，不影响功能。

### Q: 架构测试通过，为什么还不能运行？
A: 架构完全正常！只是缺少图形显示环境。选择上述任一方案即可。

### Q: 推荐哪种方案？
A:
- **开发**: 方案 B（本地机器）- 最佳体验
- **测试**: 方案 C（Xvfb）- 服务器测试
- **演示**: 方案 E（VNC）- 远程演示

## ✨ 当前状态

✅ **代码完全正常，所有测试通过！**

```
[1/7] ✓ 配置系统
[2/7] ✓ 日志系统
[3/7] ✓ 配置管理器
[4/7] ✓ 基础抽象类
[5/7] ✓ Tab 模块
[6/7] ✓ 主窗口类
[7/7] ✓ Qt 应用初始化
```

## 🎯 下一步

选择一个运行方案，然后：

1. **验证 GUI**: 确认应用正常显示
2. **开始开发**: 进入第二阶段（数据预处理模块）
3. **功能实现**: 参考 PRD.md 逐步实现功能

---

**需要帮助？**
- 查看主 README: `README.md`
- 查看 PRD: `PRD.md`
- 查看实施计划: `~/.claude/plans/whimsical-wiggling-wozniak.md`
