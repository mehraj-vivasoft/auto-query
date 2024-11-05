"use client";
import React from "react";
import useStreamResponse from "./useStreamQuery";
import { StreamDataProcessor } from "./streamDataProcessor";

const QueryPage = () => {
  const [query, setQuery] = React.useState("");
  const [responses, setResponses] = React.useState<string[]>([]);
  const { runQuery, isLoading } = useStreamResponse({
    streamCallback: setResponses,
  });

  return (
    <div className="flex flex-col items-center w-full gap-4 mt-12">
      <h1>AutoQuery</h1>
      <textarea
        name="query"
        id="query"
        placeholder="ENTER YOUR QUERY HERE"
        className="w-1/2 h-48 p-4 border border-slate-950 rounded-md text-center"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
        }}
      />
      <button
        className="bg-slate-950 text-white px-4 py-2 rounded-md"
        onClick={() => {
          console.log(query);
          runQuery(query);
        }}
      >
        Run Query
      </button>

      {responses.length > 0 && (
        <div className="w-3/4 p-4 border bg-slate-200 rounded-md text-center flex flex-col gap-2">
          {responses.map((response, index) => (
            <p
              key={index}
              className={`bg-slate-950 text-white px-4 py-4 rounded-md w-full text-md text-left tracking-wider ${
                index === responses.length - 1 ? "bg-red-950 text-yellow-300" : ""
              }`}
            >
              {/* <StreamDataProcessor text={response} /> */}
              {response}
            </p>
          ))}
        </div>
      )}

      {isLoading && <p>Loading...</p>}
    </div>
  );
};

export default QueryPage;
