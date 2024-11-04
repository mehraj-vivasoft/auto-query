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


def output_processor(query: str, output: any) -> str:

    prompt = f"""The natural language query of the user is : {query}
    After executing the query in the database, the output is as follows:
    {output}
    Now you have to process the output of the query and Give the response of the user query in natural language.
    """
    
    get_llm_logger().info(f"Processing output of the query")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a natural language processing AI that helps with SQL queries. 
            I will provide you a natural language query and the response after executing the query in the database.
            Your task is to process the output of the query and Give the response of the user query in natural language."""},
            {"role": "user", "content": prompt}
        ],
        response_format=NaturalLanguageResponse,
    )

    natural_language_response = completion.choices[0].message.parsed.natural_language_response

    get_llm_logger().info(f"Natural Language response from AI : {natural_language_response}")

    return natural_language_response
