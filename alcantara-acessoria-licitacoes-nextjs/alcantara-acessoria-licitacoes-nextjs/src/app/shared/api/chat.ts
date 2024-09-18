import type { NextApiRequest, NextApiResponse } from 'next';
import fetchChatAPI from '@/app/lib/chat/fetchChatAPI';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    console.log('API chat');
    const { edital, question } = req.body;
    const chat = await fetchChatAPI({ edital, question });
    res.status(200).json(chat);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching chat' });
  }
}
