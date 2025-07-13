import AgentMessage from './AgentMessage'
import UserMessage from './UserMessage'
import '../styles/MessageList.css'

function MessageList({ messages }) {
  // 处理讨论轮次分组
  const getDiscussionRoundLabel = (index, message, messages) => {
    // 只对讨论消息处理
    if (!message.isDiscussion || !message.discussionRound) return null;
    
    // 如果是第一条该轮次的消息，添加分隔符
    if (index === 0 || 
        messages[index - 1].discussionRound !== message.discussionRound) {
      return (
        <div className="discussion-round-separator">
          <span>第 {message.discussionRound} 轮讨论</span>
        </div>
      );
    }
    
    return null;
  };

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          发送消息开始与多个Agent聊天
        </div>
      ) : (
        messages.map((message, index) => (
          <div key={message.id}>
            {getDiscussionRoundLabel(index, message, messages)}
            {message.sender === 'user' ? (
              <UserMessage message={message} />
            ) : (
              <AgentMessage message={message} />
            )}
          </div>
        ))
      )}
    </div>
  )
}

export default MessageList