import { TableSchemaFromDB } from "../models";

export function TableSchemaAdapter(data: any): TableSchemaFromDB {
    console.log(data);
    console.log(data.columns);
    console.log(data.primary_keys);
    return {
      table_name: data.table_name,
      columns: data.columns?.map((column: any) => ({
        name: column.name,
        type: column.type,
      })),
      primary_keys: data.primary_keys,
      foreign_keys: data.foreign_keys,
      indexes: data.indexes?.map((index: any) => ({
        name: index.name,
        columns: index.columns,
      })),
    };
  }