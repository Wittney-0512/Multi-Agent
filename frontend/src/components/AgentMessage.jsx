import '../styles/AgentMessage.css'

// 为不同Agent分配不同颜色
const agentColors = {
  '顾问': '#4caf50',  // 绿色
  '批评者': '#f44336',  // 红色
  '创新者': '#2196f3',  // 蓝色
  '协调者': '#ff9800',  // 橙色
  'system': '#9e9e9e'  // 灰色
}

function AgentMessage({ message }) {
  // 获取Agent颜色，如果没有预设则使用默认颜色
  const agentColor = agentColors[message.sender] || '#9c27b0'
  
  // 确定是否需要特殊样式
  const isDiscussion = message.isDiscussion
  const isSummary = message.isSummary
  const isSystem = message.sender === 'system'
  const discussionRound = message.discussionRound

  return (
    <div className={`agent-message ${isDiscussion ? 'discussion-message' : ''} ${isSummary ? 'summary-message' : ''} ${isSystem ? 'system-message' : ''}`}>
      <div className="agent-avatar" style={{ backgroundColor: agentColor }}>
        {message.sender.slice(0, 1)}
      </div>
      <div className="message-content">
        <div className="message-header">
          <span className="agent-name" style={{ color: agentColor }}>
            {message.sender}
          </span>
          
          {discussionRound && (
            <span className="discussion-round">轮次 {discussionRound}</span>
          )}
          
          {isSummary && (
            <span className="summary-badge">讨论总结</span>
          )}
          
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