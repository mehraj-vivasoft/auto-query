'use client';

import React from 'react';
import { Message } from '../types';

interface ChatThreadProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
}

export default function ChatThread({ messages, onSendMessage }: ChatThreadProps) {
  const [inputText, setInputText] = React.useState('');
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (inputText.trim() === '') return;
    onSendMessage(inputText);
    setInputText('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="flex-grow flex flex-col bg-gray-100">
      <div className="flex-grow overflow-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[70%] p-3 rounded-lg px-4 ${
                message.sender === 'user'
                  ? 'bg-[#071e35] text-white'
                  : 'bg-[#DBE2EF] text-black'
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="flex-grow p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#192e43]"
          />
          <button
            onClick={handleSendMessage}
            className="bg-[#071e35] text-white px-4 py-2 rounded-lg hover:bg-[#192e43] transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
