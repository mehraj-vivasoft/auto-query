// app/dataset/[datasetName]/page.js
"use client";
import { useEffect, useState } from "react";

export default function DisplayJsonlData({
  params,
}: {
  params: { datasetName: string };
}) {
  const [data, setData] = useState([]);
  const [error, setError] = useState<string>();
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    if (!params.datasetName) return;

    const fetchData = async () => {
      try {
        const response = await fetch(
          `/api/jsonlData?collectionName=${params.datasetName}`
        );
        const result = await response.json();

        if (response.ok) {
          setData(result.data);
        } else {
          setError(result.error);
        }
      } catch (err) {
        console.error(err);
        setError("Failed to fetch data");
      }
    };

    fetchData();
  }, [params.datasetName]);  

  async function exportAgain() {
    try {
      setExporting(true);
      const response = await fetch(
        `/api/export-dataset?collectionName=${params.datasetName}`
      );
      const result = await response.json();

      if (response.ok) {
        try {
          const response = await fetch(
            `/api/jsonlData?collectionName=${params.datasetName}`
          );
          const result = await response.json();

          if (response.ok) {
            setData(result.data);
          } else {
            setError(result.error);
          }
        } catch (err) {
          console.error(err);
          setError("Failed to fetch data");
        }
      } else {
        setError(result.error);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to Re-Export data");
    }
    setExporting(false);
  }

  return (
    <div className="bg-[#9CDCFE]">
      <div className="flex justify-between items-center px-6 py-2 gap-2">
        <h1 className="text-center pt-4 pb-2 tracking-wider">
          DATASET : {params.datasetName}.jsonl - {data.length} entries
        </h1>
        <button
          onClick={exportAgain}
          disabled={exporting}
          className="bg-slate-900 text-white px-4 py-2 rounded-md w-max"
        >
          {exporting ? "Exporting..." : "Re-Export"}
        </button>
      </div>
      <ul className="grid md:grid-cols-2 xl:grid-cols-3 gap-4 text-xs">
        {data.map((item, index) => (
          <li
            key={index}
            className="overflow-y-hidden p-3 bg-[#202020] text-[#9CDCFE]"
          >
            <pre>{JSON.stringify(item, null, 2)}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}
