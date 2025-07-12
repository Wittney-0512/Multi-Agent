# Project Request: Multi-Agent Chat Demo

包含前后端完整项目结构，以及使用的技术栈：

- 前端：React（ Vite 创建）
- 后端：FastAPI（Python）
- 前后端分离，使用 fetch 或 axios 调用 API
- 用户每次发言后，后端调度多个 Agent 并行响应
- 每个 Agent 有自己角色设定（system prompt），并根据当前对话上下文判断是否发言
- 所有 Agent 共享一份全局历史上下文，每个 Agent 也有自己的私有上下文
- 用户可以随时插话并发起下一轮轮次
- 前端界面支持多角色分区显示（用不同颜色或头像标注每个 Agent 的回复）
- 用户发言后点击“发送”触发一次讨论循环，Agent 同时回复
- 初期先能支持 3 个 Agent，但代码结构易扩展至更多 Agent
- 所有逻辑用本地运行，无需部署


需要注意的是，OpenAI的API规范只接受"system"、"user"和"assistant"作为合法的role值，所以在准备API请求时我们仍使用这些标准值，但在内部上下文中添加额外的字段来区分不同Agent
