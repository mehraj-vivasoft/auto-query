import React, { useEffect, useState } from "react";
import { jsonlFormat, TableSchemaFromDB } from "./models";
import AutoSizedTextarea from "../components/AutoSizedTextArea";
import { getGptDescription } from "./controllers/getGptDescription";

const getSchemaInString = (tableData: TableSchemaFromDB) => {
  return `# Here is the Schema for ${
    tableData.table_name
  }:\n\n# The columns are:\n\n${tableData.columns
    ?.map((column) =>
      column.name === "CB" ||
      column.name === "CD" ||
      column.name === "MB" ||
      column.name === "MD"
        ? ``
        : `${column.name} : ${column.type}`
    )
    .join("\n")}\n\n## Primary keys are:\n\n${tableData.primary_keys?.join(
    ", "
  )}\n\n## Forign Keys Are:\n\n${tableData.foreign_keys
    ?.map(
      (key) =>
        `${key.name} : ${key.constrained_columns} -> ${key.referred_schema}.${
          key.referred_table
        }(${key.referred_columns.join(", ")})`
    )
    .join("\n")}\n\n## Indexes are:\n\n${tableData.indexes
    ?.map((index) => `${index.name} : ${index.columns.join(", ")}`)
    .join(
      "\n"
    )}\n\nRemember this details while generating query for PiHR Database`;
};

const generateTableDescriptionFromAI = async (
  tableData: TableSchemaFromDB,
  prefixMsg: string
) => {
  const schemaDetails = getSchemaInString(tableData);
  const desc = await getGptDescription(schemaDetails, prefixMsg);
  return desc;
};

const autoGenInstruction = async (
  tableName: string,
  tableData: TableSchemaFromDB,
  isAI: boolean = false
) => {
  const moduleName = tableName.split(".")[0];
  const prefixMsg =
    "In the '" +
    moduleName +
    "' module PiHR has a table named '" +
    tableName +
    "' which is used to store";
  return [
    {
      role: "system",
      content:
        "You are an expert in PiHR which is a SaaS based fully integrated HR and payroll software management system and You can generate SQL Query for PiHR Database",
    },
    {
      role: "user",
      content: isAI
        ? await generateTableDescriptionFromAI(tableData, prefixMsg)
        : prefixMsg,
    },
    {
      role: "assistant",
      content:
        "Explain the schema or details of '" +
        tableName +
        "' table So that I can generate query for PiHR Database",
    },
    {
      role: "user",
      content: getSchemaInString(tableData),
    },
  ];
};

export const JsonLMaker = ({
  addEntry,
  full_table_name,
  tableData,
}: {
  addEntry: (data: { trainingData: jsonlFormat[]; id: string }) => void;
  full_table_name: string;
  tableData: TableSchemaFromDB;
}) => {
  const roles = ["system", "user", "assistant"];
  const [selectedRole, setSelectedRole] = useState<string>("system");
  const [messages, setMessages] = useState<jsonlFormat[]>([]);
  const [instruction, setInstruction] = useState<string>(
    "You are and expert in PiHR and you can generate query for PiHR Database"
  );
  const [submittingData, setSubmittingData] = useState<boolean>(false);
  const addMessage = (role: string, content: string) => {
    setMessages([...messages, { role, content }]);
    setInstruction("");
  };
  const postMessage = async (
    tableName: string,
    trainingData: jsonlFormat[]
  ) => {
    try {
      setSubmittingData(true);
      const response = await fetch("/api/tables", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tableName, trainingData }),
      });
      const data = await response.json();
      console.log("response from mongo : ", data);
      addEntry({
        trainingData: trainingData,
        id: data.result.insertedId,
      });
      resetJsonlMaker();
    } catch (error) {
      console.error("Error saving document:", error);
    }
    setSubmittingData(false);
  };

  useEffect(() => {
    resetJsonlMaker();
  }, [full_table_name]);

  const resetJsonlMaker = () => {
    setMessages([]);
    setInstruction(
      "You are and expert in PiHR and you can generate query for PiHR Database"
    );
  };
  return (
    <div className="bg-slate-600 rounded-md w-full py-3 px-5">
      <div className="flex gap-2 flex-wrap">
        {roles.map((role, key) => (
          <button
            key={key}
            className={`px-3 py-1 rounded-md ${
              selectedRole !== role
                ? "text-slate-950 bg-white"
                : "bg-slate-950 text-white"
            }`}
            onClick={() => {
              setSelectedRole(role);
            }}
          >
            {role}
          </button>
        ))}
      </div>
      <AutoSizedTextarea
        className="w-full h-full p-4 text-white bg-transparent mt-2 focus:outline-none px-3 border-slate-300 border-[1px] rounded-md"
        placeholder="Enter Instructions Here..."
        defaultValue={instruction}
        onchange={(e) => setInstruction(e.target.value)}
      />
      <div className="flex justify-end gap-3">
        <button
          className="px-4 py-0.5 rounded-md bg-white text-slate-950"
          onClick={async () => {
            const data = await autoGenInstruction(
              full_table_name,
              tableData,
              true
            );
            setMessages(data);
          }}
        >
          AI
        </button>
        <button
          className="px-4 py-0.5 rounded-md bg-white text-slate-950"
          onClick={async () => {
            const data = await autoGenInstruction(full_table_name, tableData);
            setMessages(data);
          }}
        >
          AUTO GENERATE
        </button>
        <button
          className="px-4 py-0.5 rounded-md bg-white text-slate-950"
          onClick={() => {
            addMessage(selectedRole, instruction);
          }}
        >
          ADD
        </button>
      </div>
      <div className="flex flex-col items-start w-full">
        {messages.map((message, key) => (
          <div
            key={key}
            className="text-slate-950 bg-white w-full py-2 mt-2 rounded-md px-3"
          >
            <span className="font-semibold tracking-wider">{message.role}</span>{" "}
            : {message.content}
          </div>
        ))}
      </div>
      <button
        className="bg-slate-950 text-white w-full py-2 mt-2 rounded-md"
        onClick={async () => {
          await postMessage(full_table_name, messages);
        }}
      >
        {submittingData ? "Submitting Data" : "Save Instruction to Database"}
      </button>
    </div>
  );
};
