import React from "react";
import { TableSchemaFromDB } from "./models";

export const TableSchemaView = ({
  tableData,
}: {
  tableData: TableSchemaFromDB;
}) => {
  return (
    <div className="flex flex-col items-start md:col-span-3">
      <h1 className="font-bold text-2xl underline mt-4">
        TABLE : {tableData.table_name}
      </h1>
      <h2 className="font-bold text-2xl underline mt-4">COLUMNS</h2>
      <ul>
        {tableData.columns?.map((column) => (
          <li key={column.name}>
            <span className="font-bold tracking-wider text-md">
              {column.name}
            </span>{" "}
            : <span className="italic text-blue-600">{column.type}</span>
          </li>
        ))}
      </ul>
      <h2 className="font-bold text-2xl underline mt-4">PRIMARY KEYS</h2>
      <ul className="font-semibold tracking-wider flex gap-3 mt-2 text-sm">
        {tableData.primary_keys?.map((key) => (
          <li
            className="px-3 bg-slate-900 text-white py-1.5 rounded-md"
            key={key}
          >
            {key}
          </li>
        ))}
      </ul>
      <h2 className="font-bold text-2xl underline mt-4">FOREIGN KEYS</h2>
      <ul>
        {tableData.foreign_keys?.map((key) => (
          <li key={key.name}>
            <span className="font-semibold">{key.name}</span> :{" "}
            <span className="text-red-600">{key.constrained_columns}</span>{" "}
            {" -> "}
            <span className="text-red-600">
              {key.referred_schema}.{key.referred_table}(
              {key.referred_columns.join(", ")}
            </span>
            )
          </li>
        ))}
      </ul>
      <h2 className="font-bold text-2xl underline mt-4">INDEXES</h2>
      <ul>
        {tableData.indexes?.map((index) => (
          <li key={index.name}>
            <span className="font-semibold text-red-600">{index.name}</span> :{" "}
            {index.columns.join(", ")}
          </li>
        ))}
      </ul>
    </div>
  );
};
