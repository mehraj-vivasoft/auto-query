export interface TableSchemaFromDB {
  table_name: string;
  columns: {
    name: string;
    type: string;
  }[];
  primary_keys: string[];
  foreign_keys: {
    name: string;
    constrained_columns: string;
    referred_schema: string;
    referred_table: string;
    referred_columns: string[];
  }[];
  indexes: {
    name: string;
    columns: string[];
  }[];
}

export interface jsonlFormat {
  role: string;
  content: string;
}
