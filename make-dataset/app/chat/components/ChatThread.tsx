"use client";

import React, { useEffect } from "react";
import { Message } from "../types";
import { StreamMessageProcessor } from "./StramMessagerProcessor";
import toast from "react-hot-toast";

interface ChatThreadProps {
  companies: {
    id: string;
    name: string;
  }[];
  CompanyIsLoading: boolean;
  messages: Message[];
  onSendMessage: (text: string, company: string) => void;
}

export default function ChatThread({
  companies,
  CompanyIsLoading,
  messages,
  onSendMessage,
}: ChatThreadProps) {
  const [inputText, setInputText] = React.useState("");
  const [selectedCompany, setSelectedCompany] = React.useState<string>("1");
  const [randomLoading, setRandomLoading] = React.useState(false);
  const [randomQueries, setRandomQueries] = React.useState<
    {
      query: string;
      isSuccess: boolean;
      comment: string;
      id: string;
    }[]
  >([]);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (inputText.trim() === "") return;
    onSendMessage(inputText, selectedCompany);
    setInputText("");
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  useEffect(() => {
    const fetchQueries = async () => {
      setRandomLoading(true);
      try {
        const response = await fetch("/api/feedback?isSuccess=true");
        const data = await response.json();
        setRandomQueries(data.feedbacks);
        setRandomLoading(false);
      } catch (error) {
        console.error("Error fetching random queries:", error);
        toast.error("Error fetching random queries");
        setRandomLoading(false);
      }
    };
    fetchQueries();
  }, []);

  return (
    <div className="flex-grow flex flex-col bg-gray-100">
      <div className="flex-grow overflow-auto p-4 space-y-4">
        {messages.map(
          (message, i) =>
            message.text.length > 0 && (
              <div
                key={i}
                className={`flex ${
                  message.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[70%] rounded-lg ${
                    message.sender === "user"
                      ? "bg-[#071e35] text-white p-3 px-4" : "p-0.5"
                      // : "bg-[#DBE2EF] text-black"
                  }`}
                >
                  {message.sender === "ai" && <StreamMessageProcessor text={message?.text || ""} />}
                  {message.sender === "user" && message.text}
                </div>
              </div>
            )
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-white border-t border-gray-200 text-sm">
        <div className="flex items-center justify-start mb-2">
          {CompanyIsLoading ? (
            <div className="w-full p-2 border border-slate-950 rounded-md text-center bg-transparent">
              Loading...
            </div>
          ) : (
            <select
              className="w-full p-1 border border-slate-950 rounded-md text-center bg-transparent max-w-[500px]"
              name="companies"
              id="companies"
              value={selectedCompany}
              onChange={(e) => {
                setSelectedCompany(e.target.value);
              }}
            >
              {companies.map((company) => (
                <option key={company.id} value={company.id}>
                  {company.name}
                </option>
              ))}
            </select>
          )}
        </div>
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
