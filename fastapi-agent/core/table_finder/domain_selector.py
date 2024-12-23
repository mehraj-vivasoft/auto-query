import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

class SelectedDomainResponseFormat(BaseModel):
    selectedDomains: list[str]


def domain_selector(query: str, domains: list[str]) -> list[str]:
    """
    Returns the relevant domains from the list of domains based on the query
    """        

    prompt = f"""I have a sql db with the following schemas or domains: {domains}
    => My goal is to do the following query: {query}        
    => please help me to know that which domains are releted to the query.
    """
    
    get_llm_logger().info(f"Selecting relevent domains using llm for query: {query[:15]}...")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a sql schema or domain selctor.
             You will be given a natural language query and a list of schema or domains
             You need to choose schemas or domains releted to the query. So you will return the releted
             domain list in the given response_format."""},
            {"role": "user", "content": prompt}
        ],
        response_format=SelectedDomainResponseFormat,
    )

    selectedDomains = completion.choices[0].message.parsed.selectedDomains

    get_llm_logger().info(f"Selected domains FROM AI : {selectedDomains}")

    return selectedDomains, completion.usage.total_tokens
