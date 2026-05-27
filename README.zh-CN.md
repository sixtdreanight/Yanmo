**语言 / Language:** [English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-Hant.md) | [日本語](README.ja.md)

# 研墨 / Yanmo

[![Tests](https://img.shields.io/badge/tests-49%20passed-green)](https://github.com/sixtdreanight/Yanmo/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

**一个跑在你电脑上、数据不出门的科研助手。**

跟通用 AI 聊天不一样。研墨是专门给做科研的人用的：能拆解导师给的模糊方向、跨源追踪最新论文、交叉验证公式推导、客观评估项目方案、辅助论文写作。五个工具各有各的界面，不是塞进一个聊天框里将就。

核心就三条：**数据不出本机、公式不允许出错、支持装自己的插件。** 附带 AI 去重、AI 找思路、去 AI 味。

---

## 安装与运行

需要 Python 3.11+、Node.js 18+ 和 Ollama。

```bash
pip install -e ".[dev]"
python -m backend.main
```

后端运行在 `127.0.0.1:8000`。然后启动前端：

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。

### 桌面应用

> **注意 (2026-05):** 主要维护的前端是 React Web 应用 (`frontend/`)。
> Tauri 桌面壳 (`frontend/src-tauri/`) 和 Qt 前端 (`frontend_qt/`) 已
> **废弃**，将在未来版本中移除。维护三套前端对小型团队不可持续。
> 如果您依赖 Tauri 或 Qt 前端，请开 issue 讨论迁移到 Web 前端。

---

## 功能

顶部五个标签页（+ 右侧聊天面板）：读懂导师、追新论文、审项目、验公式、写论文。

### 读懂导师

粘贴导师的话。自动拆解为可执行任务，含排序和时间估算。每项任务可展开显示子步骤和建议资源。导师数据属机密级别，强制使用本地模型。

### 追新论文

设置研究关键词。并行抓取 ArXiv、Semantic Scholar 和 DBLP。论文以信息流展示，一键获取中文摘要。后台每小时自动更新。

三重去重（标题相似度 + arxiv_id + DOI）确保无预印本重复出现。点击「找思路」从 10+ 维度（理论性、效率、鲁棒性、公平性等）分析当前论文列表，按可信度排序标注研究空白。

### 审项目

提交项目名称和描述。从三个维度评分 — 创新性、严谨性、方法论 — 并给出具体弱点和改进建议。

### 验公式

左右分栏 LaTeX 源码与渲染预览。提交后双通道验证：基础检查（括号匹配、除零、定义域）+ SymPy 符号计算。两通道均通过才亮绿灯。不涉及任何 LLM — 纯本地符号计算。

### 写论文

生成结构化大纲，含估算字数。支持 BibTeX 粘贴解析。底部面板有「去 AI 味」工具，检测 AI 写作痕迹并自动清理。

---

## 插件系统

插件存放于 `~/.yanmo/plugins/`。通过设置 → 插件管理器加载。最低要求：`plugin.toml` + `plugin.py`。开发指南见 `plugin_schema/API.md`。支持生命周期管理、热加载/卸载和事件总线。

---

## 架构

| 组件 | 说明 |
|---|---|
| 插件引擎 | 生命周期管理、热加载/卸载、事件总线 |
| 任务调度器 | 每小时自动抓取论文 |
| WebSocket | 实时推送论文更新到前端 |
| 安全层 | 三级数据分类 + 云端操作拦截 + 审计日志 |
| 存储 | SQLite（结构化）+ ChromaDB（向量）+ 本地文件 |

## 数据安全

默认：所有操作使用本地 Ollama。云端 API 密钥为可选 — 不填就不会有任何数据离开你的机器。

- 机密数据强制本地；云端操作自动拦截
- 云端出站流量有审计日志
- 数据存储在 `~/.yanmo/`，随时备份

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python, FastAPI, SQLite, ChromaDB, SymPy, SciPy |
| 前端 | React 18, TypeScript, Vite, KaTeX |
| 桌面壳 | Tauri (Rust) |
| 字体 | Noto Sans SC, Noto Serif SC |

## 相关项目

- [myBlog](https://github.com/sixtdreanight/myBlog) — 作者博客，更多科研相关文章

## License

MIT

---

<div align="center">

**Language / 语言 / 言語**

[**English**](README.md) | [**简体中文**](README.zh-CN.md) | [**繁體中文**](README.zh-Hant.md) | [**日本語**](README.ja.md)

</div>
