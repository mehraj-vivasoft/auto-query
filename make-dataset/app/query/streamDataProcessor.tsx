import React from "react";

function parseJsonArray(input: string): object[] {
  // Fix potential JSON formatting issues by replacing single quotes with double quotes
  const formattedInput = input
    .replace(/'/g, '"') // Replace single quotes with double quotes
    .replace(/}{/g, "}|{");
  // Split by separator and parse each JSON segment
  const jsonObjects = formattedInput.split("|").map((jsonStr) => {
    try {
      return JSON.parse(jsonStr); // Parse each JSON string
    } catch (error) {
      console.error("Failed to parse JSON:", jsonStr, error);
      return null;
    }
  });

  // Filter out any null values from failed parses
  return jsonObjects.filter((obj) => obj !== null);
}

const StreamCard: React.FC<{ foundState: any }> = ({
  foundState,
}: {
  foundState: any;
}) => {
  return (
    <div className="flex gap-2 bg-slate-950 text-white px-4 py-1 rounded-md w-full my-2">
      {foundState?.status === "Selected Tables" ? (
        <>
          <h1>Selected Tables</h1>
          <p>
            {foundState?.content?.tables.map((table: string, i: number) => (
              <p key={i}>{table}</p>
            ))}
          </p>
        </>
      ) : foundState?.status === "Plan Created" ? (
        <>
          <h1>Created Plan : </h1>
          <p>{foundState?.content?.plan.toString()}</p>
        </>
      ) : foundState?.status === "Steps Created" ? (
        <>
          <h1>Created Steps : </h1>
          <p>{foundState?.content?.steps.toString()}</p>
        </>
      ) : foundState?.status === "Query Executed" ? (
        <>
          <h1>Query Executed</h1>
          <p>{foundState?.content?.query_result}</p>
        </>
      ) : foundState?.status === "Output Processed" ? (
        <>
          <h1>Output Processed</h1>
          <p>{foundState?.content?.processed_output}</p>
        </>
      ) : (
        <>
          <h1>{foundState?.status}</h1>
          <p>{foundState?.content}</p>
        </>
      )}
    </div>
  );
};

export const StreamDataProcessor = ({ text }: { text: string }) => {
  const foundStates = parseJsonArray(text);

  return (
    <>
      {foundStates.map((foundState: any, i: number) => (
        <StreamCard key={i} foundState={foundState} />
      ))}
    </>
  );
};
