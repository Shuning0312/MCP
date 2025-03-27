# ✈️ LLM-Based Travel Planner to Notion
> 基于大语言模型（LLM）+ Notion API 的旅行行程自动生成与同步工具

一个基于大语言模型（LLM）的智能旅行助手，自动生成旅行计划并同步到 Notion 数据库。你只需输入目的地和出行时间，系统将自动调用语言模型生成个性化旅行行程，并通过 Notion API 自动写入数据库，真正实现“说走就走”。

## 📦 项目结构
- `example_usage.py`：使用示例  
- `llm_connector.py`：与大语言模型的连接逻辑  
- `mcp.py`：多模态内容处理（Multi-Content Planner）基类  
- `notion_handler.py`：与 Notion API 的集成逻辑  
- `travel_mcp.py`：旅游场景下的 MCP 实现，处理具体行程计划逻辑  
- `travel_planner_app.py`：应用入口，集成各模块  
- `requirements.txt`：所需依赖库

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Shuning0312/llm-travel-planner.git
cd llm-travel-planner
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并填入以下内容：

```dotenv
OPENAI_API_KEY=your_openai_api_key
NOTION_API_KEY=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
```
> 🔑 你需要先在 Notion 创建一个集成，并获取集成 Token，绑定到你的数据库。

### 4. 运行应用
快速生成旅行计划并写入 Notion：

```bash
python example_usage.py
```

或运行主程序：

```bash
python travel_planner_app.py
```


## 🧠 项目亮点
- 🔮 自动生成旅行计划：基于 LLM（如 OpenAI GPT 系列）按需定制每日行程

- 🧭 智能日程优化：根据输入城市和出行时间合理分配景点与活动
  
- 📝 同步到 Notion：所有行程自动整理到你设定的 Notion 数据库
  
- 🔧 模块化设计：支持快速扩展为会议助手、学习计划助手等多种内容场景

## 📌 示例效果

[京都5日游计划](https://longhaired-methane-b50.notion.site/5-1c1494ada1988114b79dec88416d5b06?pvs=4)是自动写入 Notion 数据库的行程计划展示

## 🔧 可扩展方向（待更新）
✅ 接入MCP协议的规范化接口

✅ 预算估算与开销统计

✅ 多人协同旅行计划

✅ 地图 API 集成，生成路线图

✅ 行程导出为 PDF 或日历事件

✅ 接入语音助手生成旅行内容

## 🧑‍💻 开发建议

你可以从以下文件入手：
- travel_mcp.py：旅游领域内容逻辑
- llm_connector.py：对接大语言模型
- notion_handler.py：封装 Notion API 操作

## 📄 License

本项目基于 MIT License 开源，欢迎自由使用与二次开发。