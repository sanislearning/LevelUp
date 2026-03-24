import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User API
export const userAPI = {
  create: (userData) => api.post('/users', userData),
  getById: (userId) => api.get(`/users/${userId}`),
  getStats: (userId) => api.get(`/users/${userId}/stats`),
  update: (userId, userData) => api.put(`/users/${userId}`, userData),
};

// Task API
export const taskAPI = {
  classify: (title) => api.post('/tasks/classify', { title }),
  create: (taskData) => api.post('/tasks', taskData),
  getByUser: (userId, params = {}) => api.get(`/tasks/user/${userId}`, { params }),
  getTodayTasks: (userId) => api.get(`/tasks/user/${userId}/today`),
  getById: (taskId) => api.get(`/tasks/${taskId}`),
  update: (taskId, taskData) => api.put(`/tasks/${taskId}`, taskData),
  complete: (taskId) => api.post(`/tasks/${taskId}/complete`),
  delete: (taskId) => api.delete(`/tasks/${taskId}`),
};

// Health check
export const healthCheck = () => api.get('/health');

export default api;

// Made with Bob
