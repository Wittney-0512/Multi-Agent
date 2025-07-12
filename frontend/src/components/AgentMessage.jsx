import '../styles/AgentMessage.css'

// 为不同Agent分配不同颜色
const agentColors = {
  '顾问': '#4caf50',  // 绿色
  '批评者': '#f44336',  // 红色
  '创新者': '#2196f3',  // 蓝色
  'system': '#9e9e9e'  // 灰色
}

function AgentMessage({ message }) {
  // 获取Agent颜色，如果没有预设则使用默认颜色
  const agentColor = agentColors[message.sender] || '#9c27b0'

  return (
    <div className="agent-message">
      <div className="agent-avatar" style={{ backgroundColor: agentColor }}>
        {message.sender.slice(0, 1)}
      </div>
      <div className="message-content">
        <div className="message-header">
          <span className="agent-name" style={{ color: agentColor }}>
            {message.sender}
          </span>
          <span className="message-time">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>
        <div className="message-text">{message.content}</div>
      </div>
    </div>
  )
}

export default AgentMessage