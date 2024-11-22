"use client";
import React, { createContext, useContext, useEffect, useState } from "react";
import * as dotenv from 'dotenv';
dotenv.config();

interface Document {
  _id?: string;
  schemaName: string;
  tables: string[];
}

interface DataContextType {
  documents: Document[];
  loading: boolean;
  error: string | null;
  selectedSchema: number;
  setSelectedSchema: (schema: number) => void;
  selectedTable: string | null;
  setSelectedTable: (table: string) => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const TableDataProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [selectedSchema, setSelectedSchema] = useState<number>(0);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {        
        const backend_url = process.env.NEXT_PUBLIC_BACKEND_URL || "http://" + window?.location?.hostname + ":8000" ||  "http://localhost:8000";
        const response = await fetch(backend_url + "/tables");
        if (!response.ok) {
          throw new Error("Failed to fetch documents");
        }
        const data = await response.json();
        const tableData = Object.entries(data.tables);
        const finalData: Document[] = [];
        tableData.forEach(([key, value]) => {
          const doc: Document = {
            schemaName: key,
            tables: value as string[],
          };
          finalData.push(doc);
        });
        setDocuments(finalData);        
      } catch (err: any) {
        setError(err.message || "Failed to fetch documents");
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  return (
    <DataContext.Provider value={{ documents, loading, error, selectedTable, setSelectedTable, selectedSchema, setSelectedSchema }}>
      {children}
    </DataContext.Provider>
  );
};

export const useTableDataContext = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error("useDataContext must be used within a TableDataProvider");
  }
  return context;
};
