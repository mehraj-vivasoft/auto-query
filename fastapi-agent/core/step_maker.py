import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from core.query_planner import PlanList
from db.database import get_table_names
from db.get_schema_list import get_schema_list
from utils.logging_config import get_app_logger, get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class QueryStep(BaseModel):
    goal: str
    sql_query: str


class QuerySteps(BaseModel):
    steps: list[QueryStep]

def _step_to_str(step: QueryStep) -> str:
    return f"Goal: {step.goal}\nSQL Query: {step.sql_query}\n"

def steps_to_str(steps: list[QueryStep]) -> str:
    return "\n".join([_step_to_str(step) for step in steps])


def step_maker(query: str, planList: PlanList, selected_tables: list[str]) -> QuerySteps:

    tables = selected_tables
    
    get_app_logger().info(f"Getting Schema for tables: {planList.required_table_names}")    
    schemas = get_schema_list(planList.required_table_names)

    prompt = f"""I have a sql db with the following relevent tables: {tables}
    => My goal is to do the following query: {query}
    => And Here are the required schemas of the tables: {schemas}
    => I also have the following plan: {planList.plans}    
    => please help me with the write the query from the plan.
    make sure the last query is the final query that reaches the goal.
    One note if the query is about any specific company 
    first you need to take the CompanyId using this sample query: SELECT CompanyId from Security.AppClientCompany WHERE CompanyName LIKE '%name_of_company%'
    where name_of_company is the name of the company given in the user query for which you want to get the CompanyId for.
    """
    
    get_llm_logger().info(f"Generating Steps with query using llm")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a sql query generator.
             Generate SQL query from the plan given by the user.
             You have to make sure that the SQL syntext is correct and
             step by step reaches the original goal. eventually the last
             query should return the proper data that the user
             is looking for. In the last query try to avoid taking all data
             using * rather try to take data which are required
             to satisfy the query. So you will return the SQL query
             in the given response_format."""},
            {"role": "user", "content": prompt}
        ],
        response_format=QuerySteps,
    )

    query_steps = completion.choices[0].message.parsed

    get_llm_logger().info(f"Query Steps FROM AI : {query_steps}")

    return query_steps, completion.usage.total_tokens
