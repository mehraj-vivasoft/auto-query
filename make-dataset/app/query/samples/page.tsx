"use client";
import React, { useEffect } from "react";
import { FaRegCopy } from "react-icons/fa";
import toast from "react-hot-toast";
import Link from "next/link";

const SamplePage = () => {
  const [randomQueries, setRandomQueries] = React.useState<
    {
      query: string;
      isSuccess: boolean;
      comment: string;
      id: string;
    }[]
  >([]);
  const [isLoading, setIsLoading] = React.useState(false);

  const copyToClipboard = (text: string) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(
        () => {
          console.log("Text copied to clipboard successfully!");
          toast.success("Text copied to clipboard successfully!");
        },
        (err) => {
          console.error("Failed to copy text to clipboard: ", err);
          toast.error("Failed to copy text to clipboard");
        }
      );
    } else {
      // Fallback for older browsers
      const textArea = document.createElement("textarea");
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand("copy");
        console.log("Text copied to clipboard successfully!");
        toast.success("Text copied to clipboard successfully!");
      } catch (err) {
        console.error("Failed to copy text to clipboard: ", err);
        toast.error("Failed to copy text to clipboard");
      }
      document.body.removeChild(textArea);
    }
  };

  useEffect(() => {
    const fetchQueries = async () => {
      setIsLoading(true);
      const response = await fetch("/api/feedback");
      const data = await response.json();
      setRandomQueries(data.feedbacks);
      setIsLoading(false);
    };
    fetchQueries();
  }, []);

  return (
    <div className="flex flex-col items-center gap-4">
      <Link href="/">
        <img src="/auto query white.png" alt="logo" className="h-44" />
      </Link>
      <h1>SAMPLE QUERIES</h1>
      {isLoading ? (
        <div className="w-full h-full flex flex-col justify-center items-center min-h-[400px] text-2xl">
          Loading Samples...
        </div>
      ) : (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 w-full gap-4 px-4 pb-6">
          {randomQueries.map((query, index) => (
            <div
              key={index}
              onClick={() => {
                copyToClipboard(query?.query || "");
              }}
              className={
                "text-slate-950 px-6 py-4 rounded-md border-[1px] border-[#05081850] max-w-[800px] flex gap-4 justify-between hover:cursor-pointer items-center" +
                (query.isSuccess
                  ? " bg-[#44c20910] hover:bg-[#44c20925]"
                  : " bg-[#d50c2a10] hover:bg-[#d50c2a25]")
              }
            >
              <div>
                <div>{query.query}</div>
                <div className="text-xs text-slate-500">{query.comment}</div>
              </div>
              <div className="w-max">
                <FaRegCopy size={24} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SamplePage;
