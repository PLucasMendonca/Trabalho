import axios from 'axios';

const api = axios.create({
  baseURL: process.env.ALCANTARA_API_URL,
  timeout: 10_000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;
