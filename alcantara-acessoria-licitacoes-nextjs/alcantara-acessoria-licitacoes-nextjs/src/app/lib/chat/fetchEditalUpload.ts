import axios from 'axios';

export interface Response {
  data: ChatAPI[];
  message: string;
  index: string;
}

export interface ChatAPI {
  question: string;
  answer: string;
}

export interface EditalUploadProps {
  file: File;
}

const fetchEditalUpload = async ({ file }: EditalUploadProps): Promise<Response> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post<Response>('http://localhost:5000/smart/index', formData, {
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

export default fetchEditalUpload;
