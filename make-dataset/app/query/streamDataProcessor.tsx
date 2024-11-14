import React from "react";
import { BsTable } from "react-icons/bs";
import { TbBulbFilled } from "react-icons/tb";
import { LuGoal } from "react-icons/lu";
import { PiFileSqlBold } from "react-icons/pi";
import { FaFlagCheckered } from "react-icons/fa";
import { BsDatabaseFillCheck } from "react-icons/bs";
import { FaHandPointRight } from "react-icons/fa";

function parseStringToArray(input: string): string[] {
  // Remove the square brackets and split by comma
  const cleanedInput = input.replace(/[\[\]]/g, "");
  // Split the string by comma and trim any extra whitespace or quotes
  const array = cleanedInput
    .split(",")
    .map((item) => item.trim().replace(/^['"]|['"]$/g, ""));
  return array;
}

interface Plan {
  plan_description: string;
  plan_outcome: string;
}

interface Plans {
  plans: Plan[];
  required_table_names: string[];
}

interface Step {
  goal: string;
  sql_query: string;
}

interface Steps {
  steps: Step[];
}

const StreamCard: React.FC<{ foundState: string; content: string }> = ({
  foundState,
  content,
}: {
  foundState: string;
  content: string;
}) => {
  const dataObject =
    foundState === "UNKNOWN" ||
    foundState === "QUERY" ||
    foundState === "OUTPUT"
      ? null
      : foundState === "TABLES"
      ? parseStringToArray(content)
      : JSON.parse(content) || null;

  const plansObj = foundState === "PLAN" ? (dataObject as Plans) : null;
  const stepsObj = foundState === "STEPS" ? (dataObject as Steps) : null;

  return (
    <div className="flex flex-col gap-2 w-full items-center justify-center">
      {foundState === "TABLES" ? (
        <>
          <h1 className="tracking-widest">TABLE SELECTION COMPLETED</h1>
          <div className="flex flex-wrap gap-3 justify-center items-center">
            {
              // Display the tables as a list
              dataObject
                ? dataObject?.map((table: string, index: number) => (
                    <div
                      className="bg-slate-200 text-slate-950 px-4 py-2 rounded-lg flex gap-3 items-center"
                      key={index}
                    >
                      <BsTable />
                      <div>{table}</div>
                    </div>
                  ))
                : content
            }
          </div>
        </>
      ) : foundState === "PLAN" ? (
        <>
          <h1 className="tracking-widest">PLAN CREATION COMPLETED</h1>
          {plansObj ? (
            <div className="flex flex-col gap-4">
              {plansObj.plans.map((plan, index) => (
                <div
                  key={index}
                  className="flex flex-col p-4 rounded-lg gap-4 bg-slate-200 text-slate-950"
                >
                  <div className="flex gap-2 items-end bg-slate-950 text-slate-200 w-fit px-4 py-2 rounded-lg">
                    <TbBulbFilled size={24} />
                    <div className="text-md -mb-0.5">Plan {index + 1}</div>
                  </div>
                  <h2 className="text-center">{plan.plan_description}</h2>
                  <div className="flex gap-2 items-center bg-slate-950 text-slate-200 px-4 py-2 rounded-xl justify-center">
                    <div className="flex gap-2 w-max">
                      <LuGoal size={24} />
                      <span className="font-bold">Outcome:</span>
                    </div>
                    <span>{plan.plan_outcome}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>{content}</p>
          )}
        </>
      ) : foundState === "STEPS" ? (
        <>
          <h1 className="tracking-widest">STEPS CREATION COMPLETED</h1>
          {stepsObj ? (
            <div className="flex flex-col gap-4">
              {stepsObj.steps.map((step, index) => (
                <div
                  key={index}
                  className="flex flex-col p-4 rounded-lg gap-4 bg-slate-200 text-slate-950"
                >
                  <div className="flex gap-2 items-end bg-slate-950 text-slate-200 w-fit px-4 py-2 rounded-lg">
                    <FaFlagCheckered size={24} />
                    <div className="text-md -mb-0.5">Step {index + 1}</div>
                  </div>
                  <h2 className="text-center">{step.goal}</h2>
                  <div className="flex gap-3 items-center bg-slate-950 text-slate-200 px-4 py-3 rounded-xl justify-center">
                    <div className="w-max">
                      <PiFileSqlBold size={32} />
                    </div>
                    <span>{step.sql_query}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>{content}</p>
          )}
        </>
      ) : foundState === "QUERY" ? (
        <>
          <h1 className="tracking-widest">QUERY EXECUTED SUCCESSFULLY</h1>
          <div className="flex gap-2 items-center bg-slate-950 text-slate-200 px-4 py-2 rounded-xl border-[1px] border-[#ffffff30]">
            <div className="flex gap-2 w-max">
              <BsDatabaseFillCheck size={24} />
              <span className="font-bold">Query Raw Result:</span>
            </div>
            <span>{content}</span>
          </div>
        </>
      ) : foundState === "OUTPUT" ? (
        <>
          <h1 className="tracking-widest">OUTPUT PROCESSED</h1>
          <div className="flex gap-2 items-center bg-slate-950 text-slate-200 px-4 py-2 rounded-xl border-[1px] border-[#ffffff30]">
            <div className="flex gap-2 w-max">
              <FaHandPointRight size={24} />
              <span className="font-bold">Output:</span>
            </div>
            <span>{content}</span>
          </div>
        </>
      ) : (
        <div className="text-center">{content}</div>
      )}
    </div>
  );
};

export const StreamDataProcessor = ({ text }: { text: string }) => {
  const foundState = text.startsWith("Selected Tables are:")
    ? "TABLES"
    : text.startsWith("Created Plan is :")
    ? "PLAN"
    : text.startsWith("Created Steps are :")
    ? "STEPS"
    : text.startsWith("Query Result:")
    ? "QUERY"
    : text.startsWith("Output Processed:")
    ? "OUTPUT"
    : "UNKNOWN";

  if (foundState === "TABLES") {
    const tables = text.replace("Selected Tables are:", "");
    return <StreamCard foundState={foundState} content={tables} />;
  }

  if (foundState === "PLAN") {
    const plan = text.replace("Created Plan is :", "");
    return <StreamCard foundState={foundState} content={plan} />;
  }

  if (foundState === "STEPS") {
    const steps = text.replace("Created Steps are :", "");
    return <StreamCard foundState={foundState} content={steps} />;
  }

  if (foundState === "QUERY") {
    const query = text.replace("Query Result:", "");
    return <StreamCard foundState={foundState} content={query} />;
  }

  if (foundState === "OUTPUT") {
    const output = text.replace("Output Processed:", "");
    return <StreamCard foundState={foundState} content={output} />;
  }

  return <StreamCard foundState={foundState} content={text} />;
};
