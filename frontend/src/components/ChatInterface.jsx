import { useState, useEffect, useRef } from 'react'
import MessageInput from './MessageInput'
import MessageList from './MessageList'
import { sendMessage } from '../services/api'
import '../styles/ChatInterface.css'

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [showContext, setShowContext] = useState(false)
  const [contextData, setContextData] = useState(null)
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

  // 获取上下文数据
  const fetchContext = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/context');
      const data = await response.json();
      setContextData(data);
    } catch (error) {
      console.error("获取上下文失败:", error);
      setContextData({ error: "获取上下文失败" });
    }
  };

  // 切换上下文显示状态
  const toggleContext = () => {
    const newState = !showContext;
    setShowContext(newState);
    if (newState) {
      fetchContext();
    }
  };

  return (
    <div className="chat-interface">
      <div className="context-controls">
        <button 
          onClick={toggleContext}
          className="context-button"
        >
          {showContext ? "隐藏上下文" : "显示上下文"}
        </button>
      </div>
      
      {showContext && contextData && (
        <div className="context-viewer">
          <h3>全局上下文 ({contextData.global_context_length || 0}条消息)</h3>
          <pre className="context-content">
            {contextData.error || JSON.stringify(contextData.global_context, null, 2)}
          </pre>
          
          <h3>Agent私有上下文</h3>
          {contextData.agents && Object.entries(contextData.agents).map(([name, data]) => (
            <div key={name} className="agent-context">
              <h4>{name} ({data.private_context_length || 0}条消息)</h4>
              <pre className="context-content">
                {JSON.stringify(data.private_context, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      )}
      
      <MessageList messages={messages} />
      <div ref={messagesEndRef} />
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  )
}

export default ChatInterface