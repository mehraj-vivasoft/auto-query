export interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
}

export interface ChatThread {
  id: number;
  title: string;
  messages: Message[];
}
