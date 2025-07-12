import AgentMessage from './AgentMessage'
import UserMessage from './UserMessage'
import '../styles/MessageList.css'

function MessageList({ messages }) {
  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          发送消息开始与多个Agent聊天
        </div>
      ) : (
        messages.map((message) => (
          message.sender === 'user' ? (
            <UserMessage key={message.id} message={message} />
          ) : (
            <AgentMessage 
              key={message.id} 
              message={message}
              // 可以传递更多属性给AgentMessage
            />
          )
        ))
      )}
    </div>
  )
}

export default MessageList