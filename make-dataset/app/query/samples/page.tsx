"use client";
import React from "react";
import { randomQueries } from "../randomQueries";
import { FaRegCopy } from "react-icons/fa";
import toast from "react-hot-toast";

const SamplePage = () => {
  return (
    <div className="flex flex-col items-center gap-4">
      <a href="/">
        <img src="/auto query white.png" alt="logo" className="h-44" />
      </a>
      <h1>SAMPLE QUERIES</h1>
      <div className="flex flex-col gap-4 px-4 pb-6">
        {randomQueries.map((query, index) => (
          <div
            key={index}
            onClick={() => {
              navigator.clipboard.writeText(query);
              toast.success("Query copied to clipboard");
            }}
            className="bg-[#05081810] text-slate-950 px-6 py-4 rounded-md border-[1px] border-[#05081850] max-w-[800px] flex gap-4 justify-between hover:cursor-pointer hover:bg-[#05081825]"
          >
            <div>{query}</div>
            <FaRegCopy size={24} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default SamplePage;
