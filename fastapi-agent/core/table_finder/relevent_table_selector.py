import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class SelectedTableResponseFormat(BaseModel):
    selectedTables: list[str]


def relevent_table_selector(query: str, tables: list[str]) -> list[str]:
    """
    Returns the relevant tables from the list of tables based on the query
    """        

    prompt = f"""I have a sql db which contains following tables: {tables}
    => My goal is to do the following query: {query}    
    => please help me to know that which tables are needed for the query.
    """
    
    get_llm_logger().info(f"Selecting relevent tables from {tables[0].split('.')[0]} domain")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a sql table selctor for making sql queries.
             You will be given a natural language query and a list of tables
             You need to choose releted tables .So, you will return the releted
             table list in the given response_format."""},
            {"role": "user", "content": prompt}
        ],
        response_format=SelectedTableResponseFormat,
    )

    selectedTables = completion.choices[0].message.parsed.selectedTables

    get_llm_logger().info(f"Selected tables FROM AI : {selectedTables}")

    return selectedTables
