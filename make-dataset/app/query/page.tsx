"use client";
import React from "react";
import useStreamResponse from "./useStreamQuery";
import { StreamDataProcessor } from "./streamDataProcessor";
import { FaRandom } from "react-icons/fa";
import { randomQueries } from "./randomQueries";

const QueryPage = () => {
  const [query, setQuery] = React.useState("");
  const [responses, setResponses] = React.useState<string[]>([]);
  const { runQuery, isLoading } = useStreamResponse({
    streamCallback: setResponses,
  });

  return (
    <div className="grid md:grid-cols-3 w-full min-h-screen">
      <div className="px-6 flex flex-col justify-start items-center md:min-h-screen gap-6 bg-slate-200 pb-6">
        <a href="/">
          <img
            src="auto query white.png"
            alt="auto query"
            className="h-36 mt-12"
          />
        </a>
        <textarea
          name="query"
          id="query"
          placeholder="ENTER YOUR QUERY HERE"
          className="w-full h-32 md:h-64 p-4 border border-slate-950 rounded-md text-center bg-transparent"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
          }}
        />
        <div className="w-full flex items-center gap-3 justify-end -mt-3">
          <button
            className="bg-slate-950 text-white px-4 py-2 rounded-md flex items-center gap-2"
            onClick={() => {
              setQuery(
                randomQueries[Math.floor(Math.random() * randomQueries.length)]
              );
            }}
          >
            <FaRandom />
            Random
          </button>
          <button
            className="bg-slate-950 text-white px-4 py-2 rounded-md"
            onClick={() => {
              console.log(query);
              runQuery(query);
            }}
          >
            Run Query
          </button>
        </div>
      </div>

      <div className="md:col-span-2 p-4 bg-slate-950 text-white rounded-md text-center flex flex-col gap-2 overflow-y-scroll">
        {responses.map((response, index) => (
          <p
            key={index}
            className={`px-4 py-4 rounded-md w-full text-md text-left tracking-wider ${
              index === responses.length - 1
                ? "text-red-950 bg-yellow-300 font-bold"
                : "bg-[#ffffff08] text-white border-[1px] border-[#ffffff25]"
            }`}
          >
            <StreamDataProcessor text={response} />
            {/* {response} */}
          </p>
        ))}
        {isLoading && <p className="text-cyan-400">Loading...</p>}
      </div>
    </div>
  );
};

export default QueryPage;
