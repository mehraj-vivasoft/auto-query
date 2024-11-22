"use client";
import { useTableDataContext } from "@/context/TablesContext";
import { useEffect, useState } from "react";
import { jsonlFormat, TableSchemaFromDB } from "./models";
import { TableSchemaAdapter } from "./controllers/tableSchemaAdapter";
import { NEXT_PUBLIC_AI_BACKEND } from "@/lib/consts";

export const useTableData = () => {
  const { selectedTable, selectedSchema, documents } = useTableDataContext();
  const [full_table, setFullTable] = useState<string>("");
  const [tableData, setTableData] = useState<TableSchemaFromDB>();
  const [addedDataset, setAddedDataset] = useState<
    {
      trainingData: jsonlFormat[];
      id: string;
    }[]
  >([]);

  const addEntry = (entry: { trainingData: jsonlFormat[]; id: string }) => {
    setAddedDataset([...addedDataset, entry]);
  };

  const removeEntry = (id: string) => {
    setAddedDataset(addedDataset.filter((entry) => entry.id !== id));
  }

  // Table changed!
  useEffect(() => {
    if (!selectedTable) {
      console.log("Table not found");
    } else {
      const schema_name = documents[selectedSchema].schemaName;
      setFullTable(
        `${schema_name === "base" ? "" : schema_name + "."}${selectedTable}`
      );
      // resetJsonlMaker();
    }
  }, [selectedTable, documents, selectedSchema]);

  // call to get table schema
  useEffect(() => {
    if (full_table.length > 2) {
      const backend_url = NEXT_PUBLIC_AI_BACKEND || "http://" + window.location.hostname + ":8000" ||  "http://localhost:8000";
      fetch(`${backend_url}/schema`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          table_names: [full_table],
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setTableData(TableSchemaAdapter(data.schema[0]));
        });
      fetch("/api/tables?tableName=" + full_table, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          setAddedDataset(data.addedTrainingData || []);
          console.log(data);
        });
    }
  }, [full_table]);

  return {
    tableData,
    addEntry,
    addedDataset,
    removeEntry
  };
};
