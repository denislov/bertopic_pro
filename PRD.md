BERTopic Pro 主题建模分析桌面终端 - 产品需求文档 (PRD)
1. 产品背景与定位
1.1 项目背景
科研人员在处理大规模文本数据时，常面临环境配置难、算法参数多、可视化不直观等问题。本项目旨在开发一款基于 PySide6 的原生桌面应用，集成 BERTopic 完整流，提供开箱即用的主题分析能力。
1.2 核心价值
 * 零代码操作：通过 GUI 完成复杂的建模过程。
 * 本地化安全：核心计算在本地完成，保障敏感研究数据的安全。
 * 专业级可视化：内置高性能 Chromium 内核，完美渲染交互式科研图表。
2. 功能模块详细需求
2.1 模块一：数据导入与预处理 (Tab 1)
 * 文件导入：
   * 支持 .csv 和 .xlsx 格式。
   * 读取后在 QTableWidget 中展示前 50 行数据预览。
 * 字段映射：
   * 用户需指定一列作为“分析文本”，一列作为“时间戳”（可选，用于动态主题分析）。
 * 中文优化：
   * 集成 Jieba 分词。
   * 支持自定义停用词加载。
2.2 模块二：BERTopic 核心建模 (Tab 2)
 * 组件化参数配置：
   * Embedding: 下拉选择模型（Sentence-Transformers 或 API 模式）。
   * UMAP: 调整 n_neighbors, n_components, min_dist。
   * HDBSCAN: 调整 min_topic_size, min_samples。
 * 异步运行机制：
   * 点击“开始建模”后，UI 必须保持响应。
   * 使用 QThread 封装算法，通过信号（Signal）将实时日志和进度发送至 UI 底部的控制台。
2.3 模块三：结果可视化交互 (Tab 3)
 * 图表渲染引擎：使用 QtWebEngineView。
 * 图表类型：
   * 话题间距离图（Intertopic Distance Map）。
   * 话题层次聚类图（Hierarchical Clustering）。
   * 话题关键词权重图（Topic Word Scores）。
   * 话题演化趋势图（Topics over Time，若有时间戳数据）。
 * 导出功能：右键或按钮导出为独立 HTML 文件。
2.4 模块四：系统设置与管理 (Tab 4)
 * 模型仓库：
   * 显示本地已缓存的 HuggingFace 模型路径。
   * 模型下载状态监控（使用进度条展示 requests 或 huggingface_hub 的下载进度）。
 * LLM Provider：
   * 配置 OpenAI, Ollama 或 智谱 AI。
   * 用于对提取的话题进行语义总结（Representation）。
 * 硬件设置：
   * 检测 CUDA 是否可用，支持 CPU/GPU 切换。
3. 界面设计 (UI/UX)
 * 布局模式：
   * 导航区：顶部水平选项卡（QTabWidget）。
   * 主工作区：根据 Tab 切换。
   * 底部控制台：常驻深色背景终端（QPlainTextEdit），展示标准 Python 日志输出。
 * 视觉风格：
   * 主色调：#1976d2（专业蓝）。
   * 字体：思源黑体/微软雅黑（支持跨平台 Noto 字体）。
   * 组件样式：通过 QSS（Qt Style Sheets）实现圆角卡片化设计。
4. 技术规格
 * GUI 框架：PySide6 6.5.0+。
 * 浏览器内核：PySide6.QtWebEngineWidgets (Chromium 引擎)。
 * 多线程模型：QThread + Worker 对象。
 * 日志系统：自定义 logging.Handler 重定向至 UI 线程。
 * 存储方案：本地配置文件（.ini 或 .json）。
5. 打包与交付
 * 工具链：PyInstaller 或 Nuitka。
 * 资源处理：
   * 所有 QSS 文件、图标、HTML 模板需作为静态资源打包。
   * 确保 WebEngine 运行时所需的动态库正确包含。
6. 验证过程与质量标准
 * UI 响应性验证：在建模运行期间，用户必须能够点击其他 Tab 查看设置，界面不得出现“无响应”白屏。
 * 渲染验证：Plotly 图表必须能够正常响应鼠标悬停（Hover）和缩放（Zoom）操作。
 * 并发验证：当用户在下载模型时，仍可进行本地文本预处理操作。

BERTopic Pro 项目目录结构
bertopic_app/
├── main.py                 # 应用入口：初始化 QApplication，加载主窗口
├── config.py               # 全局配置：路径、API Keys、默认参数
├── app/
│   ├── ui/                 # 界面模块 (纯代码布局)
│   │   ├── init.py
│   │   ├── main_window.py  # 主窗口：承载 QTabWidget 和底部的日志控制台
│   │   ├── styles/         # 样式表
│   │   │   └── theme.qss   # 定义界面颜色、圆角、按钮样式
│   │   └── tabs/           # 各选项卡独立类
│   │       ├── init.py
│   │       ├── preprocess.py # 数据导入与预处理界面
│   │       ├── modeling.py   # 模型参数配置界面
│   │       ├── visual.py     # WebView 可视化展示界面
│   │       └── settings.py   # LLM 与系统配置界面
│   ├── core/               # 核心逻辑
│   │   ├── worker.py       # QThread 子类：负责 BERTopic 的耗时计算
│   │   ├── processor.py    # 文本处理逻辑 (Pandas/NLP)
│   │   └── model_manager.py# 模型加载与管理
│   └── utils/              # 工具类
│       ├── logger.py       # 自定义 Log Handler，将日志定向到 UI
│       └── helpers.py      # 文件读写辅助
├── data/                   # 数据存放
│   ├── raw/                # 原始文件
│   └── cache/              # 存放 Plotly 生成的临时 HTML 文件
├── models/                 # 本地存储训练好的模型
├── requirements.txt
└── .env                    # 环境变量