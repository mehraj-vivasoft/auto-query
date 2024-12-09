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

def _plan_to_str(plan: Plan) -> str:
    print(plan)
    return f"Plan Description: {plan.plan_description}\nPlan Outcome: {plan.plan_outcome}\n"

def plan_list_to_str(plans: list[Plan]) -> str:
    print(plans)    
    return "\n".join([_plan_to_str(plan) for plan in plans])

def query_planner(query: str, selected_tables: list[str]) -> PlanList:        

    prompt = f"""I have a sql db with the following relevent tables: {selected_tables}
    I want to do the following query: {query}
    please help me with the plan for the query and also tell me how to use 
    tables that are needed or releted for the query.
    """
    
    # One note if the query is about any specific company 
    # first you need to take the CompanyId using this sample query: SELECT CompanyId from Security.AppClientCompany WHERE CompanyName LIKE '%name_of_company%'
    # where name_of_company is the name of the company given in the user query for which you want to get the CompanyId for.
    
    get_llm_logger().info(f"Planning the query using llm")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a sql query planner.
            Guide the user by generating a plan for the given query. You will return
            an array of plans with required table names which contains
            the plan description and outcome in the given response_format. 
            For each plan, You have to provide a plan description 
            and the outcome of the plan."""},
            {"role": "user", "content": prompt}
        ],
        response_format=PlanList,
    )

    query_plan = completion.choices[0].message.parsed

    get_llm_logger().info(f"Query Plan FROM AI : {query_plan}")

    return query_plan, completion.usage.total_tokens
