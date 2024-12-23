import React from "react";
import { BsTable } from "react-icons/bs";
import { TbBulbFilled } from "react-icons/tb";
import { LuGoal } from "react-icons/lu";
import { PiFileSqlBold } from "react-icons/pi";
import { FaFlagCheckered } from "react-icons/fa";
import { BsDatabaseFillCheck } from "react-icons/bs";
import { FaHandPointRight } from "react-icons/fa";
import SQLResultTable from "@/app/components/SQLResultTable";
import { BarChartBasic } from "@/components/graphs/BarChart";

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

interface BarRaw {
  bars: {
    keyName: string;
    value: number;
  }[];
  key_title: string;
  value_title: string;
  bar_chart_title: string;
  bar_chart_description: string;
}

function transformChartData(input: BarRaw) {
  // Dynamically map key and value titles
  const keyTitle = input.key_title.replace(/\s+/g, ""); // Remove spaces
  const valueTitle = input.value_title.replace(/\s+/g, ""); // Remove spaces

  return {
    chartData: input.bars
      .filter((item) => item.value > 0) // Exclude entries with value 0
      .map((item) => ({
        [keyTitle]: item.keyName, // Use dynamic key for EmployeeName
        [valueTitle]: item.value, // Use dynamic key for TotalLeaveDays
      })),
    title: input.bar_chart_title,
    subtitle: input.bar_chart_description,
  };
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
  const barChartObj = foundState === "BAR" ? (dataObject as BarRaw) : null;
  const transformedData = barChartObj ? transformChartData(barChartObj) : null;

  //   console.log("FoundState", foundState);
  //   console.log("DataObject", dataObject);
  //   console.log("content", content);

  return foundState === "TABLES" ||
    foundState === "PLAN" ||
    foundState === "STEPS" ||
    foundState === "QUERY" ||
    foundState === "OUTPUT" ||
    foundState === "BAR" ? (
    <div
      className={
        "flex flex-col gap-2 w-full items-center justify-center px-4 py-3 bg-[#DBE2EF] rounded-lg"
      }
    >
      {foundState === "TABLES" ? (
        <>
          <h1 className="tracking-widest w-full">Selected Tables:</h1>
          <div className="w-full flex flex-wrap gap-3 justify-start items-center">
            {
              // Display the tables as a list
              dataObject
                ? dataObject?.map((table: string, index: number) => (
                    <div
                      className="bg-slate-200 text-slate-950 border-2 border-slate-950 px-4 py-2 rounded-lg flex gap-3 items-center"
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
          <h1 className="tracking-widest w-full">
            Here is my plan for your query:
          </h1>
          {plansObj ? (
            <div className="flex flex-col gap-4">
              {plansObj.plans.map((plan, index) => (
                <div
                  key={index}
                  className="flex flex-col p-4 rounded-lg gap-4 bg-slate-200 text-slate-950 border-2 border-slate-950 text-sm"
                >
                  <div className="flex gap-2 items-end bg-slate-950 text-slate-200 w-fit px-4 py-2 rounded-lg items-center">
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
          <h1 className="tracking-widest w-full">
            Here are the steps for your query:
          </h1>
          {stepsObj ? (
            <div className="flex flex-col gap-4">
              {stepsObj.steps.map((step, index) => (
                <div
                  key={index}
                  className="flex flex-col p-4 rounded-lg gap-4 bg-slate-200 text-slate-950 border-2 border-slate-950"
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
          <h1 className="tracking-widest w-full">
            I have executed your query:
          </h1>
          <div className="flex gap-2 items-center bg-slate-950 text-slate-200 px-4 py-2 rounded-xl border-[1px] border-[#ffffff30]">
            <div className="flex gap-2 w-max">
              <BsDatabaseFillCheck size={24} />
              <span className="font-bold">Query Raw Result:</span>
            </div>
            <span>{content}</span>
          </div>
          <div className="bg-slate-950 w-full text-slate-200 px-4 py-2 rounded-lg">
            <div className="flex gap-3 items-end bg-slate-950 text-slate-200 w-fit py-2 rounded-lg">
              <FaFlagCheckered size={24} />
              <div className="text-sm">Here is the SQL Result as Table</div>
            </div>
            <SQLResultTable resultString={content} />
          </div>
        </>
      ) : foundState === "OUTPUT" ? (
        <>
          <h1 className="tracking-widest w-full">Response to your query:</h1>
          <div className="flex gap-2 items-center bg-slate-950 text-slate-200 px-4 py-2 rounded-xl border-[1px] border-[#ffffff30]">
            <div className="flex gap-2 w-max">
              <FaHandPointRight size={24} />
              <span className="font-bold">Output:</span>
            </div>
            <span>{content}</span>
          </div>
        </>
      ) : foundState === "BAR" ? (
        <>
          <h1 className="tracking-widest">BAR CREATION COMPLETED</h1>
          {barChartObj && transformedData ? (
            <div className="">
              <BarChartBasic
                chartData={transformedData.chartData}
                title={transformedData.title}
                subtitle={transformedData.subtitle}
              />
            </div>
          ) : (
            <p>{content}</p>
          )}
        </>
      ) : (
        <></>
      )}
    </div>
  ) : (
    <div className="text-center text-xs italic text-muted-foreground">
      {content}
    </div>
  );
};

export const StreamMessageProcessor = ({ text }: { text: string }) => {
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
    : text.startsWith("Bar Chart is:")
    ? "BAR"
    : "UNKNOWN";

  // console.log("content to process : ", text);

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

  if (foundState === "BAR") {
    const bar = text.replace("Bar Chart is:", "");
    return <StreamCard foundState={foundState} content={bar} />;
  }

  return <StreamCard foundState={foundState} content={text} />;
};
