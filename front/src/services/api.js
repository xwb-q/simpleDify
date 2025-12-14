import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Workflow APIs
export const getWorkflows = () => api.get('/workflows/');
export const getWorkflow = (id) => api.get(`/workflows/${id}`);
export const createWorkflow = (data) => api.post('/workflows/', data);
export const updateWorkflow = (id, data) => api.put(`/workflows/${id}`, data);
export const deleteWorkflow = (id) => api.delete(`/workflows/${id}`);
export const executeWorkflow = (id, inputData = null) => {
  const data = inputData ? { input_data: inputData } : {};
  return api.post(`/workflows/${id}/execute`, data);
};

// Model APIs
export const callQwenPlus = (data) => api.post('/models/qwen-plus', data);

export default api;