import { useState, useEffect, useRef } from 'react'
import MessageInput from './MessageInput'
import MessageList from './MessageList'
import { sendMessage } from '../services/api'
import '../styles/ChatInterface.css'

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // 自动滚动到底部
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async (content) => {
    if (!content.trim()) return

    // 添加用户消息到列表
    const userMessage = {
      id: Date.now(),
      sender: 'user',
      content,
      timestamp: new Date().toISOString()
    }
    
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // 调用API获取Agent回复
      const responses = await sendMessage(content)
      
      // 添加Agent回复到消息列表
      const agentMessages = responses.map((response, index) => ({
        id: Date.now() + index + 1,
        sender: response.agent_name,
        content: response.content,
        timestamp: new Date().toISOString()
      }))
      
      setMessages(prev => [...prev, ...agentMessages])
    } catch (error) {
      console.error('获取回复失败:', error)
      // 添加错误消息
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'system',
        content: '获取Agent回复时发生错误，请稍后重试。',
        timestamp: new Date().toISOString()
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-interface">
      <MessageList messages={messages} />
      <div ref={messagesEndRef} />
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  )
}

export default ChatInterface