import { useState } from 'react'
import '../styles/MessageInput.css'

function MessageInput({ onSendMessage, isLoading }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading) {
      onSendMessage(message)
      setMessage('')
    }
  }

  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="输入消息..."
        disabled={isLoading}
        className="message-input-field"
      />
      <button 
        type="submit" 
        disabled={isLoading || !message.trim()} 
        className="send-button"
      >
        {isLoading ? '处理中...' : '发送'}
      </button>
    </form>
  )
}

export default MessageInput