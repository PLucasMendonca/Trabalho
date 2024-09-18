import axios from 'axios';
import { Response } from './fetchEditalUpload';

export interface Message {
  question: string;
  answer: string;
}

export interface ChatAPI {
  question: string;
  answer: string;
}

export interface ChatProps {
  edital: string;
  question: string;
}

const fetchChatAPI = async ({ edital, question }: ChatProps): Promise<Response> => {
  try {
    const formData = new FormData();
    formData.append('edital', edital);
    formData.append('question', question);

    const response = await axios.post<Response>('http://localhost:5000/smart/chat', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch answer:', error);
    throw new Error('Failed to fetch answer');
  }
};

export default fetchChatAPI;
