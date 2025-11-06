import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for API aggregation
  headers: {
    'Content-Type': 'application/json',
  },
});

export const checkIP = async (ipAddress) => {
  try {
    const response = await api.get(`/check-ip/${ipAddress}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Failed to fetch IP threat data'
    );
  }
};

export const reportIP = async (ipData) => {
  try {
    const response = await api.post('/report-ip', ipData);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 'Failed to report IP'
    );
  }
};

export default api;
