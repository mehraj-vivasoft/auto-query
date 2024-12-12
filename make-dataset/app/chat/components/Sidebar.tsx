"use client";

import React from "react";
import Image from "next/image";
import { MdEdit, MdDelete } from "react-icons/md";
import { FaSave } from "react-icons/fa";
import { ChatThread } from "../types";
import Link from "next/link";

interface SidebarProps {
  threads: ChatThread[];
  activeThreadId: number;
  isSidebarOpen: boolean;
  onThreadSelect: (threadId: number) => void;
  onCreateThread: () => void;
  onDeleteThread: (threadId: number) => void;
  onUpdateThreadTitle: (threadId: number, newTitle: string) => void;
}

export default function Sidebar({
  threads,
  activeThreadId,
  isSidebarOpen,
  onThreadSelect,
  onCreateThread,
  onDeleteThread,
  onUpdateThreadTitle,
}: SidebarProps) {
  const [editingThreadId, setEditingThreadId] = React.useState<number | null>(
    null
  );
  const [editThreadTitle, setEditThreadTitle] = React.useState("");

  const startEditingThread = (thread: ChatThread) => {
    setEditingThreadId(thread.id);
    setEditThreadTitle(thread.title);
  };

  const saveThreadTitle = () => {
    if (editThreadTitle.trim() === "") return;
    if (editingThreadId) {
      onUpdateThreadTitle(editingThreadId, editThreadTitle.trim());
      setEditingThreadId(null);
    }
  };

  return (
    <div
      id="sidebar"
      className={`${
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      } md:translate-x-0 fixed md:relative min-w-fit w-64 h-full bg-[#071e35] text-white p-4 flex flex-col transition-transform duration-300 ease-in-out z-40`}
    >
      <div className="mb-6 flex justify-center">
        <Link href="/">
          <Image
            src="/auto query black.png"
            alt="Logo"
            width={250}
            height={250}
            className="rounded-full"
          />
        </Link>
      </div>

      <button
        onClick={onCreateThread}
        className="bg-[#DBE2EF] hover:bg-[#071e35] text-[#071e35] hover:text-[#DBE2EF] hover:border-[#DBE2EF] border-2 py-2 px-4 rounded-lg mb-4 transition"
      >
        + New Chat
      </button>

      <div className="flex-grow overflow-auto">
        {threads.map((thread) => (
          <div
            key={thread.id}
            className={`p-3 cursor-pointer rounded-lg mb-2 flex justify-between items-center ${
              activeThreadId === thread.id
                ? "bg-[#F9F7F7] text-[#071e35]"
                : "hover:bg-[#DBE2EF50] hover:text-[#ffffff]"
            }`}
          >
            {editingThreadId === thread.id ? (
              <div className="flex items-center w-full">
                <input
                  type="text"
                  value={editThreadTitle}
                  onChange={(e) => setEditThreadTitle(e.target.value)}
                  onBlur={saveThreadTitle}
                  onKeyPress={(e) => e.key === "Enter" && saveThreadTitle()}
                  className="flex-grow bg-transparent border-b border-[#071e35] text-[#071e35] focus:outline-none"
                  autoFocus
                />
                <FaSave
                  onClick={saveThreadTitle}
                  className="text-green-500 hover:text-green-700 cursor-pointer"
                  size={18}
                />
              </div>
            ) : (
              <div
                onClick={() => onThreadSelect(thread.id)}
                className="flex-grow"
              >
                {thread.title}
              </div>
            )}

            {editingThreadId !== thread.id && (
              <div className="flex space-x-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    startEditingThread(thread);
                  }}
                  className="text-blue-500 hover:text-blue-700"
                >
                  <MdEdit />
                </button>
                {threads.length > 1 && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteThread(thread.id);
                    }}
                    className="text-red-500 hover:text-red-700"
                  >
                    <MdDelete />
                  </button>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
