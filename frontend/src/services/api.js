import axios from 'axios'

const BASE_URL = '/api'

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 120000, // 2 min for AI calls
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.response.use(
  res => res.data,
  err => {
    const msg =
      err.response?.data?.error ||
      (err.code === 'ECONNABORTED' ? 'Request timed out. The AI is taking longer than usual.' : null) ||
      err.message ||
      'An unexpected error occurred'
    return Promise.reject(new Error(msg))
  }
)

const api = {
  analyzeCareer: (profile) => client.post('/analyze-career', profile),
  chat: (payload) => client.post('/chat', payload),
  compareCareers: (payload) => client.post('/compare-careers', payload),
  updateProgress: (payload) => client.post('/update-progress', payload),
  health: () => client.get('/health'),
}

export default api
