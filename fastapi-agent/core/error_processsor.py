import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class NaturalLanguageResponse(BaseModel):
    natural_language_response: str


def error_processor(query: str, errorMsg: str, sql_query: str) -> str:

    prompt = f"""The natural language query of the user is : {query}
    and the SQL query is : {sql_query}
    After executing the query in the database, there has error as follows:
    {errorMsg}
    Now, process the error message and explain the error and why it occured in natural language. 
    In the explanation do not use technical terms. just try to explain the error in easy way that
    the user can understand and if the query contains ? then tell the user to which values are missing in the query.
    The user should easyly understand the error and why it occured and what data is missing in the query.
    """
    
    get_llm_logger().info(f"Processing output of the query")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a natural language processing AI that helps explaining errors in SQL queries. 
            I will provide you a natural language query, a sql query and ther error message after executing the query in the database.
            Your task is to process the error message and explain the error and why it occured to the user in natural language."""},
            {"role": "user", "content": prompt}
        ],
        response_format=NaturalLanguageResponse,
    )

    natural_language_response = completion.choices[0].message.parsed.natural_language_response

    get_llm_logger().info(f"Natural Language response from AI : {natural_language_response}")

    return natural_language_response, completion.usage.total_tokens
