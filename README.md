# 研墨 / Yanmo

[![Tests](https://img.shields.io/badge/tests-49%20passed-green)](https://github.com/sixtdreanight/Yanmo/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

**A privacy-first research assistant that runs locally on your machine — your data never leaves your computer.**

**一个跑在你电脑上、数据不出门的科研助手。**

跟通用 AI 聊天不一样。研墨是专门给做科研的人用的：能拆解导师给的模糊方向、跨源追踪最新论文、交叉验证公式推导、客观评估项目方案、辅助论文写作。五个工具各有各的界面，不是塞进一个聊天框里将就。

核心就三条：**数据不出本机、公式不允许出错、支持装自己的插件。** 附带 AI 去重、AI 找思路、去 AI 味。

桌面应用，不是网页。Windows、Linux、macOS 都能跑。

## 安装与运行

依赖 Python 3.11+、Node.js 18+、Ollama。

```bash
pip install -e ".[dev]"
python -m backend.main
```

后端跑在 `127.0.0.1:8000`。然后启动前端：

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。

### 桌面应用

装好 [Rust](https://rustup.rs) 之后：

```bash
cd frontend
cargo tauri dev      # 开发，带热重载
cargo tauri build    # 打包成 exe / app / deb
```

Tauri 窗口启动时会自动拉起 Python 后端，关了窗口自动杀掉进程。

## 功能

顶部五个标签：读懂导师、追新论文、审项目、验公式、写论文。右边侧栏有个聊天窗。

### 读懂导师

粘贴导师的原话，自动拆成可执行任务，排好顺序，估好时间。每个任务展开能看到子步骤和建议资源。

导师发言数据标记为机密，强制走本地模型。

### 追新论文

设好研究方向的关键词，自动从 ArXiv、Semantic Scholar、DBLP 三个源并行抓取。论文以信息流方式排列，一键生成中文摘要。每小时后台自动更新一次。

内置三重去重（标题相似度 + arxiv_id + DOI），同一个预印本不会出现两次。点"找思路"会分析当前论文列表，从理论、效率、鲁棒性、公平性等十几个维度标注研究空白，按置信度排序。

### 审项目

填项目名称和描述，从创新性、合理性、方法论三个维度评分，指出不足和改进方向。

### 验公式

LaTeX 源码和渲染预览左右分栏。提交后双通道验证：基本检查（括号匹配、除零、定义域）加 SymPy 符号计算。两道都过才亮绿灯。

不走 LLM，纯本地符号计算。

### 写论文

生成结构化大纲（带预估字数），支持 BibTeX 粘贴解析。底部有"去 AI 味"工具，粘贴文本自动检测 AI 写作痕迹——词汇密度、破折号、三段式、句子均匀度——给出评分，然后自动清洗。

## 插件

用户插件放在 `~/.yanmo/plugins/`，到设置→插件管理里加载。最少需要 `plugin.toml` 和 `plugin.py` 两个文件。开发指南见 `plugin_schema/API.md`。

## 架构

| 组件 | 说明 |
|------|------|
| 插件引擎 | 生命周期管理、热加载/卸载、事件总线 |
| 任务调度器 | 定时自动抓取论文，每小时一次 |
| WebSocket | 论文更新实时推送到前端 |
| 安全层 | 三级数据分类 + 云端操作拦截 + 审计日志 |
| 存储 | SQLite（结构化）+ ChromaDB（向量）+ 本地文件 |

## 数据安全

默认所有操作走本地 Ollama。云端 API Key 需自行填写，不填就不联网。

- 机密数据强制本地，操作自动拦截
- 云端外发有审计日志
- 数据存在 `~/.yanmo/`，随时备份

## 技术栈

| 层 | 选型 |
|---|---|
| 后端 | Python, FastAPI, SQLite, ChromaDB, SymPy, SciPy |
| 前端 | React 18, TypeScript, Vite, KaTeX |
| 桌面壳 | Tauri (Rust) |
| 字体 | Noto Sans SC, Noto Serif SC |

## License

MIT
