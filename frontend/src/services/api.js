import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const sendMessage = async (content) => {
  try {
    const response = await apiClient.post('/chat', { content })
    return response.data
  } catch (error) {
    console.error('API错误:', error)
    throw error
  }
}

export const startDiscussion = async (topic, maxRounds = 3) => {
  try {
    const response = await apiClient.post('/discussion', { 
      topic, 
      max_rounds: maxRounds 
    })
    return response.data
  } catch (error) {
    console.error('启动讨论API错误:', error)
    throw error
  }
}

export const getDiscussionStatus = async () => {
  try {
    const response = await apiClient.get('/discussion/status')
    return response.data
  } catch (error) {
    console.error('获取讨论状态错误:', error)
    throw error
  }
}