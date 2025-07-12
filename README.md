# Project Request: Multi-Agent Chat Demo

请为我生成一个包含前后端的完整项目结构，使用以下技术栈：

- 前端：React（推荐用 Vite 创建）
- 后端：FastAPI（使用 Python）
- 前后端分离，使用 fetch 或 axios 调用 API
- 用户每次发言后，后端调度多个 Agent 并行响应
- 每个 Agent 有自己角色设定（system prompt），并根据当前对话上下文判断是否发言
- 所有 Agent 共享一份全局历史上下文，每个 Agent 也有自己的私有上下文
- 用户可以随时插话并发起下一轮轮次
- 前端界面支持多角色分区显示（用不同颜色或头像标注每个 Agent 的回复）
- 用户发言后点击“发送”触发一次讨论循环，Agent 同时回复
- 项目初期只需要支持 3 个 Agent，代码结构需易于扩展到更多 Agent
- 所有逻辑用本地运行即可，无需部署

请一步步生成：
1. 项目文件结构说明
2. FastAPI 后端：agent 管理器、主接口、模型模拟
3. React 前端：简单对话 UI，多 Agent 回复展示
4. 如何本地运行 demo（Python 和 Node 两边都说明）

后续我会逐步要求你细化具体模块，请保持结构清晰，可运行，注释清楚。
