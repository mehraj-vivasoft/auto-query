import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from db.database import get_table_names
from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class Plan(BaseModel):
    plan_description: str
    plan_outcome: str


class PlanList(BaseModel):
    plans: list[Plan]    
    required_table_names: list[str]


def query_planner(query: str, selected_tables: list[str]) -> PlanList:

    prompt = f"""I have a sql db with the following tables: {selected_tables}
    I want to do the following query: {query}
    please help me with the plan for the query and also tell me the tables 
    that are needed or releted for the query.
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a sql query planner.
            Guide the user through plan given query. You have to provide a
            plan description and the outcome of the plan. So you will return
            an array of plans with required table names which contains
            the plan description and outcome in the given response_format."""},
            {"role": "user", "content": prompt}
        ],
        response_format=PlanList,
    )

    query_plan = completion.choices[0].message.parsed

    get_llm_logger().info(f"Query Plan FROM AI : {query_plan}")

    return query_plan
