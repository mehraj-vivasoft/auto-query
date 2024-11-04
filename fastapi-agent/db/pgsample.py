# from databases import Database
# import pymssql
# DATABASE_URL = "postgresql://postgres:helloworld%3F@localhost:5432/school"
# pymssql.connect(server='localhost', user='SA', password='Helloworld1?',
# database='huduri_production20240930')


    # columns = []
    # for column in columnData:
    #     columns.append(
    #         {
    #             "name": column["name"],
    #             "type": column["type"],
    #         }
    #     )

    # foreign_keys = []
    # for fk in fk_Data:
    #     foreign_keys.append(
    #         {
    #             "name": fk["name"],
    #             "constrained_columns": fk["constrained_columns"],
    #             "referred_columns": fk["referred_columns"],
    #             "referred_table": fk["referred_table"]
    #         }
    #     )

    # schema = {
    #     "table_name": table_name,
    #     "columns": columns,
    #     "foreign_keys": foreign_keys
    # }
    # logger.info(f"Schema for table {table_name}: {schema}")
    # return schema