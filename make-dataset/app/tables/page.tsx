"use client";
import { AddedDataset } from "./AddedDataset";
import { JsonLMaker } from "./JsonLMaker";
import { TableSchemaView } from "./TableSchemaView";
import { useTableData } from "./useTableData";

const TablePage = () => {
  const { tableData, addEntry, addedDataset, removeEntry } = useTableData();

  return (
    <div className="py-4 px-6">
      {tableData && (
        <div className="grid md:grid-cols-5 gap-6 md:gap-2">
          <TableSchemaView tableData={tableData} />
          <div className="md:col-span-2">
            <JsonLMaker
              full_table_name={tableData.table_name}
              addEntry={addEntry}
              tableData={tableData}
            />
            <AddedDataset
              addedDataset={addedDataset}
              tableName={tableData.table_name}
              removeEntry={removeEntry}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default TablePage;
