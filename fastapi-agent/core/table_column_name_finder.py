import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from core.step_maker import QuerySteps
from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class ColumnNames(BaseModel):
    column_names: list[str]


async def table_column_name_finder(query: str, queryList: QuerySteps):    

    prompt = f"""
    => My goal is to do the following query: {query}    
    => I wrote the following sql query:
     {queryList.steps[-1].sql_query}
    => I want to get the column names of the output of the query so that
    I can use the column names to show them in the UI. Make sure that the number
    of column names matches the number of columns in the output. Return the
    column names in the given response format.
    """

    get_llm_logger().info("GETTING COLUMN NAMES USING LLM")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a sql query column name finder.
             You will be given a natural language query, a sql query for that. 
             Find the column names of the tables in the query and return the
             list of column names in the given response format."""},
            {"role": "user", "content": prompt}
        ],
        response_format=ColumnNames,
    )

    column_names = completion.choices[0].message.parsed.column_names

    get_llm_logger().info(f"COLUMN NAMES FROM AI : {column_names}")

    return column_names, completion.usage.total_tokens
