# 科研助手 — 设计规格

## 目标

面向科研人员的本地优先、保密优先的全流程助手。覆盖：理解导师需求、追踪最新文献、评估项目质量、验证公式方程、辅助论文写作。

## 核心约束

- 数据不出本机（默认所有操作走本地）
- 用户完全控制云端 API 使用
- 插件化架构，支持社区扩展
- Python 学术生态 + React 现代前端

---

## 架构

### 整体架构

```
前端 (React Workbench)
  ↕ localhost REST API
Python 核心引擎 (FastAPI)
  ├ 插件注册器 → 插件容器 (术语/文献/评估/公式/写作)
  ├ 事件总线   → 插件间异步通信
  ├ LLM 路由   → 本地 Ollama ↔ 云端 API 切换
  ├ 安全管理   → 数据分级 + 操作拦截 + 外发审计
  └ 存储层     → SQLite + ChromaDB + 本地文件系统
```

核心引擎只做路由、调度、存储，不包含业务逻辑。每个插件 = 独立 Python 包 + 前端组件包，通过标准接口注册。

### 插件接口规范

**后端接口（每个插件必须实现）：**

```python
class Plugin:
    name: str
    display_name: str
    version: str

    def on_load(self, bus, config): ...
    def on_unload(self): ...
    def get_routes(self) -> APIRouter: ...
    def get_commands(self) -> list: ...
```

**前端接口（每个插件提供）：**

```typescript
interface PluginPanel {
  name: string;
  component: React.FC;
  icon: string;
}

interface PluginCommands {
  [command: string]: (args: string[]) => Promise<string>;
}
```

**事件总线频道（插件间通信，禁止直接 import）：**

- `paper.saved` / `paper.updated` — 文献库变更
- `term.added` / `term.updated` — 术语库变更
- `formula.verified` — 公式验证完成
- `project.evaluated` — 评估报告生成

**注册清单（plugin.toml）：**

```toml
[plugin]
name = "literature"
display_name = "追新论文"
version = "1.0.0"
dependencies = ["knowledge-base"]
```

---

## 功能面板

顶部标签栏：`[读懂导师] [追新论文] [审项目] [验公式] [写论文]`

全局侧边面板：`我的资料`（知识库浏览）、`问一问`（对话助手）

### 读懂导师（term-advisor）

- 输入导师原话 → 结构化解析为可执行任务
- 术语搜索 + 知识图谱可视化
- 领域术语消歧（同名不同义）
- 自建术语库浏览与管理
- 强制走本地模型（数据为机密级）

### 追新论文（literature）

- ArXiv / 顶会新论文推送流
- 关键词追踪 + 热点趋势图
- 论文一键摘要 + 与自身项目关联分析
- 定时抓取、离线阅读

### 审项目（evaluator）

- 输入项目描述 → 创新性 / 合理性 / 方法论评分
- 与文献库对比 → 定位差异与不足
- 评估报告导出

### 验公式（formula）

- 所见即所得 LaTeX 编辑器（源码 | 实时渲染 分栏）
- SymPy 符号验证 + SciPy 数值验证双通道交叉比对
- 公式库归档与复用
- 不走 LLM，纯符号/数值计算

### 写论文（paper-writer）

- 结构化大纲编辑器
- 引文管理（BibTeX / 本地文献库联动）
- 语言润色建议
- 格式合规检查（会议/期刊模板）

---

## 数据安全

### 数据分级

| 级别 | 范围 | 云端 LLM | 存储 |
|------|------|----------|------|
| 机密 🔴 | 导师私密信息、未公开数据、专利材料 | 禁止 | 加密本地 |
| 审慎 🟡 | 项目思路、论文草稿 | 用户逐次放行 | 本地 |
| 公开 🟢 | 已发表文献标题/摘要 | 可选 | 本地 |

### 三层保护

1. **入口拦截** — 导入内容时询问数据级别，机密级自动标记
2. **操作拦截** — 机密数据 + 云端路由 = 直接阻断
3. **外发审计** — 通过云端 API 发送的内容记录日志（时间、模型、内容 hash），不含原文

### 默认安全策略

- 安装后默认全部走本地 Ollama
- 云端 API Key 需用户主动填写
- 不收集遥测，不联网检查更新（用户主动触发才检查）
- 所有数据存 `~/.research-assistant/`，用户可随时备份/删除

### LLM 路由隐私警告

首次设置云端 API 时，红底警告卡片，需勾选"我已理解"才能继续：

> 发送到云端 API 的数据会离开你的电脑。导师未公开的研究思路、实验数据、专利相关材料请勿使用云端模型处理。如不确定，请先咨询导师。

运行时提醒：当功能风险为中/高且使用云端模型时，每次会话显示一次提示。

---

## 技术选型

### 前端

- React 18 + TypeScript + Vite
- Golden Layout（多面板拖拽工作台）
- KaTeX（公式渲染）
- ECharts（趋势图表）

### 后端

- FastAPI（Python 3.11+）
- SymPy（符号计算）+ SciPy（数值验证）
- ChromaDB（向量存储）+ sentence-transformers（本地嵌入）
- feedparser + aiohttp（文献抓取）
- ollama SDK + httpx（统一 LLM 客户端抽象）
- 自研 EventBus + 插件注册器

### 存储

- SQLite — 结构化数据（配置、元数据、引文库）
- ChromaDB — 向量数据（论文全文、术语、公式语义检索）
- 本地文件系统 — 原始文件（PDF、笔记、导出报告）

### 桌面壳（后期可选）

- Electron / Tauri 包裹前端为独立窗口应用

---

## 项目目录结构

```
research-assistant/
├── backend/
│   ├── core/                 # 核心引擎
│   │   ├── engine.py         # 插件生命周期管理
│   │   ├── event_bus.py      # 事件总线
│   │   ├── llm_router.py     # LLM 路由
│   │   ├── storage.py        # SQLite + ChromaDB 接口
│   │   ├── security.py       # 数据分级 + 操作拦截
│   │   └── config.py         # 全局配置
│   ├── plugins/              # 内置插件
│   │   ├── term_advisor/
│   │   ├── literature/
│   │   ├── evaluator/
│   │   ├── formula/
│   │   └── paper_writer/
│   ├── api/gateway.py        # FastAPI 统一入口
│   └── main.py
├── frontend/
│   └── src/
│       ├── core/             # 工作台框架
│       ├── plugins/          # 前端插件组件
│       └── shared/           # 通用组件
├── plugin_schema/            # 插件开发规范
├── docs/superpowers/specs/
├── pyproject.toml
└── package.json
```

---

## 构建顺序

1. 核心引擎（插件注册器、事件总线、LLM 路由、存储、安全）
2. 读懂导师 插件
3. 追新论文 插件
4. 验公式 插件
5. 审项目 插件
6. 写论文 插件
7. 桌面壳（可选）
