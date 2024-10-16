import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from core.query_planner import PlanList
from db.database import get_schema_list, get_table_names
from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

class QueryStep(BaseModel):
    goal: str
    sql_query: str    
    
class QuerySteps(BaseModel):
    steps: list[QueryStep]
    
def step_maker(query: str, planList: PlanList):
    
    tables = get_table_names()
    schemas = get_schema_list(planList.required_table_names)
    
    prompt = f"""I have a sql db with the following tables: {tables}
    => My goal is to do the following query: {query}
    => And Here are the required schemas of the tables: {schemas}
    => I also have the following plan: {planList.plans}    
    
    => please help me with the write the query from the plan. make sure the last query is the final query that reaches the goal.
    """
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a sql query generator. Generate SQL query from the plan given by the user. You have to make sure that the SQL syntext is correct and step by step reaches the original goal. So you will return the SQL queries in the given response_format."},
            {"role": "user", "content": prompt}
        ],
        response_format=QuerySteps,
    )

    query_steps = completion.choices[0].message.parsed
    
    get_llm_logger().info(f"Query Steps FROM AI : {query_steps}")
    
    return query_steps