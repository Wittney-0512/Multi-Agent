import '../styles/UserMessage.css'

function UserMessage({ message }) {
  return (
    <div className="user-message">
      <div className="message-content">
        <div className="message-text">{message.content}</div>
        <div className="message-time">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  )
}

export default UserMessage