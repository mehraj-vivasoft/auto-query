"use client";
import React from "react";
import { jsonlFormat } from "./models";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import AutoSizedTextarea from "../components/AutoSizedTextArea";
import remarkBreaks from "remark-breaks";

export const DatasetSlice = ({
  data,
  tableName,
  removeEntry,
}: {
  tableName: string;
  data: {
    trainingData: jsonlFormat[];
    id: string;
  };
  removeEntry: (id: string) => void;
}) => {
  const [isEdit, setIsEdit] = React.useState<boolean>(false);
  const [updating, setUpdating] = React.useState<boolean>(false);
  const [deleting, setDeleting] = React.useState<boolean>(false);
  const [dataset, setDataset] = React.useState<{
    trainingData: jsonlFormat[];
    id: string;
  }>(data);

  const updateDataset = async () => {
    try {
      setUpdating(true);
      const response = await fetch("/api/tables", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...dataset, tableName }),
      });
      if (response.ok) {
        console.log("Dataset updated successfully");
      } else {
        console.error("Failed to update dataset");
      }
    } catch (error) {
      console.error("Error updating dataset:", error);
    }
    setUpdating(false);
  };

  const deleteDataset = async () => {
    try {
      setDeleting(true);
      const response = await fetch("/api/tables", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: dataset.id }),
      });
      if (response.ok) {
        console.log("Dataset deleted successfully");
      } else {
        console.error("Failed to delete dataset");
      }
    } catch (error) {
      console.error("Error deleting dataset:", error);
    }
    removeEntry(dataset.id);
    setDeleting(false);
  };

  return (
    <>
      <div className="flex justify-end mt-1 gap-3">
        <button
          className="px-3 py-0.5 bg-red-800 text-white rounded-lg"
          onClick={() => {
            deleteDataset();
          }}
        >
          {deleting ? "Deleting..." : "Delete"}
        </button>
        {isEdit && (
          <button
            className="px-3 py-0.5 bg-slate-950 text-white rounded-lg"
            onClick={() => {
              setIsEdit(false);
            }}
          >
            Cancel
          </button>
        )}
        <button
          className="px-3 py-0.5 bg-slate-950 text-white rounded-lg"
          onClick={() => {
            if (isEdit) {
              updateDataset();
            }
            setIsEdit(!isEdit);
          }}
        >
          {updating ? "Updating..." : isEdit ? "Save" : "Edit"}
        </button>
      </div>
      {dataset?.trainingData?.map((message, key) => (
        <div
          key={dataset.id + key}
          className="text-slate-950 bg-white w-full py-2 my-2 rounded-md px-3"
        >
          {isEdit ? (
            <div className="flex flex-col gap-2 items-start">
              <div className="bg-slate-950 text-white px-3 py-0.5 rounded-md">
                {message.role}
              </div>
              <AutoSizedTextarea
                className="w-full bg-transparent border-[1px] border-slate-950 focus:outline-none px-3 py-1 rounded-md h-auto"
                defaultValue={message.content}
                onchange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                  const newDataset = dataset.trainingData.map((item, index) => {
                    if (index === key) {
                      return { ...item, content: e.target.value };
                    }
                    return item;
                  });
                  setDataset({ ...dataset, trainingData: newDataset });
                }}
              />
            </div>
          ) : (
            <>
              <span className="font-semibold tracking-wider text-red-700">
                {message.role}
              </span>{" "}
              {": "}
              <span>
                <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
                  {message.content}
                </ReactMarkdown>
              </span>
            </>
          )}
        </div>
      ))}
    </>
  );
};
