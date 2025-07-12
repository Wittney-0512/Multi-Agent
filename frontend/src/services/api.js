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
    return response.data.responses
  } catch (error) {
    console.error('API错误:', error)
    throw error
  }
}