import axios from 'axios';

// Use environment variables for Create React App
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const createPropertyWithTenant = async (data: any) => {
  return api.post('/properties', data);
};

export const fetchProperties = async () => {
  const response = await api.get('/properties');
  return response.data;
};

export const fetchTenants = async () => {
  const response = await api.get('/tenants');
  return response.data;
};

export const createTenant = async (data: any) => {
  return api.post('/tenants', data);
};

export const updateProperty = async (id: number, data: any) => {
  return api.put(`/properties/${id}`, data);
};

export const deleteProperty = async (id: number) => {
  return api.delete(`/properties/${id}`);
};

export const updateTenant = async (id: number, data: any) => {
  return api.put(`/tenants/${id}`, data);
};

export const deleteTenant = async (id: number) => {
  return api.delete(`/tenants/${id}`);
}; 