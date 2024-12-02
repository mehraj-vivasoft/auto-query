"use client";
import React, { useEffect } from "react";
import useStreamResponse from "./useStreamQuery";
import { StreamDataProcessor } from "./streamDataProcessor";
import { FaRandom } from "react-icons/fa";
import Link from "next/link";
import toast from "react-hot-toast";
import { FaPlay } from "react-icons/fa";
import useCompanies from "./useComapnies";

const QueryPage = () => {
  const [query, setQuery] = React.useState("");
  const [responses, setResponses] = React.useState<string[]>([]);
  const [showReport, setShowReport] = React.useState(false);
  const { runQuery, isLoading } = useStreamResponse({
    streamCallback: setResponses,
  });
  const [comment, setComment] = React.useState("");
  const [randomLoading, setRandomLoading] = React.useState(false);
  const [submitLoading, setSubmitLoading] = React.useState(false);

  const [randomQueries, setRandomQueries] = React.useState<
    {
      query: string;
      isSuccess: boolean;
      comment: string;
      id: string;
    }[]
  >([]);

  const { companies, CompanyIsLoading } = useCompanies();
  const [selectedCompany, setSelectedCompany] = React.useState<string>("0");

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

  const submitReport = async (isSuccess: boolean) => {
    try {
      setSubmitLoading(true);
      const response = await fetch("/api/feedback", {
        method: "POST",
        body: JSON.stringify({
          query,
          isSuccess,
          comment,
        }),
      });
      const data = await response.json();
      toast.success("Report submitted successfully");
      console.log(data);
      setSubmitLoading(false);
    } catch (error) {
      console.error("Error submitting report:", error);
      toast.error("Error submitting report");
      setSubmitLoading(false);
    }
  };

  return (
    <div className="grid md:grid-cols-3 w-full min-h-screen">
      <div className="px-6 flex flex-col justify-start items-center md:min-h-screen gap-6 bg-slate-200 pb-6">
        <Link href="/">
          <img
            src="auto query white.png"
            alt="auto query"
            className="h-36 mt-12"
          />
        </Link>
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
        <div className="-mt-2 flex items-center justify-center">
          {CompanyIsLoading ? (
            <div className="w-full p-2 border border-slate-950 rounded-md text-center bg-transparent">
              Loading...
            </div>
          ) : (
            <select
              className="w-full p-2 border border-slate-950 rounded-md text-center bg-transparent"
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
        <div className="w-full flex items-center gap-3 justify-center flex-wrap tracking-wider">
          <button
            className="bg-slate-950 text-white px-4 py-2 rounded-lg hover:text-slate-950 hover:bg-white border-2 hover:border-slate-950"
            onClick={() => {
              setShowReport(!showReport);
            }}
          >
            Report
          </button>
          <button
            className="bg-slate-950 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:text-slate-950 hover:bg-white border-2 hover:border-slate-950"
            disabled={randomLoading}
            onClick={() => {
              setQuery(
                randomQueries[Math.floor(Math.random() * randomQueries.length)]
                  .query
              );
            }}
          >
            <FaRandom />
            {randomLoading ? "Loading..." : "Random"}
          </button>
          <button
            className="bg-slate-950 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:text-slate-950 hover:bg-white border-2 hover:border-slate-950"
            disabled={isLoading}
            onClick={() => {
              console.log(query);
              runQuery("I am an admin of CompanyId " + selectedCompany + ". " + query);
            }}
          >
            <FaPlay />
            {isLoading ? "Querying..." : "Run"}
          </button>
        </div>
        {showReport && (
          <div className="flex flex-col px-4 py-2 gap-2 w-full">
            <h1>REPORT QUERY</h1>
            <div>Query: {query}</div>
            <textarea
              name="report"
              id="report"
              placeholder="ENTER YOUR COMMENT HERE"
              value={comment}
              onChange={(e) => {
                setComment(e.target.value);
              }}
              className="w-full h-32 p-4 border border-slate-950 rounded-md text-center bg-transparent"
            />
            <button
              className="bg-green-900 text-white px-4 py-2 rounded-md"
              disabled={submitLoading}
              onClick={() => {
                submitReport(true);
              }}
            >
              {submitLoading ? "loading..." : "Submit Success"}
            </button>
            <button
              className="bg-red-900 text-white px-4 py-2 rounded-md"
              disabled={submitLoading}
              onClick={() => {
                submitReport(false);
              }}
            >
              {submitLoading ? "loading..." : "Submit Failure"}
            </button>
          </div>
        )}
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
