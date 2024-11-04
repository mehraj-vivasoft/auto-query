"use client";
import React, { useEffect } from "react";
import { jsonlFormat } from "./models";
import { DatasetSlice } from "./DatasetSlice";

export const AddedDataset = ({
  addedDataset,
  tableName,
  removeEntry
}: {
  addedDataset: {
    trainingData: jsonlFormat[];
    id: string;
  }[];
  tableName: string;
  removeEntry: (id: string) => void;
}) => {

  useEffect(() => {
    console.log("DATASET RENDERING: ", addedDataset);
  }, [addedDataset]);

  return (
    <div className="mt-4">
      <h2 className="font-bold text-2xl underline">PREPARED DATASET</h2>
      {addedDataset && addedDataset.length === 0 && (
        <div className="mt-4 text-xl">
          NO TRAINING DATA ADDED FOR {tableName}
        </div>
      )}
      {addedDataset?.map((data) => (
          <div
            key={data.id}
            className="mt-4 bg-slate-200 border-slate-950 border-2 rounded-lg px-4 py-2"
          >
            <DatasetSlice data={data} tableName={tableName} removeEntry={removeEntry}/>
          </div>
        ))}
    </div>
  );
};
