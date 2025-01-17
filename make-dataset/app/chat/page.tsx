"use client";

import React, { useState, useEffect } from "react";
import { HiMenuAlt2 } from "react-icons/hi";
import { IoMdClose } from "react-icons/io";
import ChatThread from "./components/ChatThread";
import Sidebar from "./components/Sidebar";
import { ChatThread as ChatThreadType, Message } from "./types";
import useCompanies from "../query/useComapnies";
import useStreamResponseForChat from "./useStreamQueryForChat";

export default function ChatPage() {
  const [threads, setThreads] = useState<ChatThreadType[]>([
    { id: 1, title: "New Chat 1", messages: [] },
  ]);
  const [activeThreadId, setActiveThreadId] = useState(1);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { companies, CompanyIsLoading } = useCompanies();
  const [responses, setResponses] = useState<string[]>([]);
  const { runQuery, isLoading, setIsLoading } = useStreamResponseForChat({
    streamCallback: setResponses,
  });

  const activeThread = threads.find((thread) => thread.id === activeThreadId)!;

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const sidebar = document.getElementById("sidebar");
      const toggleButton = document.getElementById("sidebarToggle");

      if (
        sidebar &&
        toggleButton &&
        !sidebar.contains(event.target as Node) &&
        !toggleButton.contains(event.target as Node)
      ) {
        setIsSidebarOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    console.log("responses", responses);
    const formattedResponse: Message[] = responses.map((response) => ({
      id: Date.now(),
      text: response.replace("<<GGNOTAI>>", ""),
      sender: response.includes("<<GGNOTAI>>") ? "user" : "ai",
    }));
    setThreads((prevThreads) =>
      prevThreads.map((thread) =>
        thread.id === activeThreadId
          ? {
              ...thread,
              messages: formattedResponse,
            }
          : thread
      )
    );
  }, [responses]);

  const handleSendMessage = async (text: string, company: string) => {
    // const newUserMessage: Message = {
    //   id: Date.now(),
    //   text,
    //   sender: "user",
    // };

    // const newAIMessage: Message = {
    //   id: Date.now() + 1,
    //   text: `AI response to: ${text}`,
    //   sender: "ai",
    // };

    // const updatedThreads = threads.map((thread) =>
    //   thread.id === activeThreadId
    //     ? {
    //         ...thread,
    //         messages: [...thread.messages, newUserMessage],
    //       }
    //     : thread
    // );

    // setThreads(updatedThreads);

    setResponses([...responses, "<<GGNOTAI>>" + text]);
    setTimeout(() => {
      setIsLoading(true);
      runQuery("I am an admin of CompanyId " + company + ". " + text);
      // runQuery(text);
    }, 1000);
  };

  const handleCreateThread = () => {
    const newThreadId = Date.now();
    setThreads([
      ...threads,
      {
        id: newThreadId,
        title: `New Chat ${threads.length + 1}`,
        messages: [],
      },
    ]);
    setActiveThreadId(newThreadId);
    setIsSidebarOpen(false);
  };

  const handleDeleteThread = (threadId: number) => {
    if (threads.length <= 1) return;

    const updatedThreads = threads.filter((thread) => thread.id !== threadId);
    setActiveThreadId(updatedThreads[0].id);
    setThreads(updatedThreads);
  };

  const handleUpdateThreadTitle = (threadId: number, newTitle: string) => {
    const updatedThreads = threads.map((thread) =>
      thread.id === threadId ? { ...thread, title: newTitle } : thread
    );

    setThreads(updatedThreads);
  };

  const handleThreadSelect = (threadId: number) => {
    setActiveThreadId(threadId);
    setIsSidebarOpen(false);
  };

  return (
    <div className="flex h-screen relative">
      <button
        id="sidebarToggle"
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-[#071e35] text-white rounded-lg"
      >
        {isSidebarOpen ? <IoMdClose size={24} /> : <HiMenuAlt2 size={24} />}
      </button>

      <Sidebar
        threads={threads}
        activeThreadId={activeThreadId}
        isSidebarOpen={isSidebarOpen}
        onThreadSelect={handleThreadSelect}
        onCreateThread={handleCreateThread}
        onDeleteThread={handleDeleteThread}
        onUpdateThreadTitle={handleUpdateThreadTitle}
      />

      <ChatThread
        companies={companies}
        CompanyIsLoading={CompanyIsLoading}
        messages={activeThread.messages}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
}
