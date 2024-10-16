import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from core.query_planner import PlanList
from core.step_maker import QuerySteps
from db.database import get_schema_list, get_table_names
from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class FixQuery(BaseModel):
    query: str


async def query_fixer(
    query: str, planList: PlanList, queryList: QuerySteps, error_message: str
):

    tables = get_table_names()
    schemas = get_schema_list(planList.required_table_names)

    # => I did followed the following steps to do the query: {queryList}    

    prompt = f"""I have a sql db with the following tables: {tables}
    => My goal is to do the following query: {query}
    => And Here are the required schemas of the tables: {schemas}
    => I did the following query:
     {queryList.steps[-1].sql_query}
    => But, I got this error while running the final query: {error_message}
    => please fix the final query and return a query which is correct
     and also reaches the goal.
    """

    get_llm_logger().info("FIXING QUERY")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a sql query fixer.
             You will be given a query with a query plan and a
             error message while running the last and final combined query.
             Fix the sql query to reach the goal and return in the query
             according to the response format ."""},
            {"role": "user", "content": prompt}
        ],
        response_format=FixQuery,
    )

    fixed_query = completion.choices[0].message.parsed.query

    get_llm_logger().info(f"FIXED QUERY FROM AI : {fixed_query}")

    return fixed_query
