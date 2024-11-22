import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

from core.query_planner import PlanList
from core.step_maker import QuerySteps
from db.get_schema_list import get_schema_list
from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class FixQuery(BaseModel):
    fixed_query: str


async def query_fixer(
    query: str, planList: PlanList, queryList: QuerySteps, error_message: str, selected_tables: list[str]
):

    tables = selected_tables
    schemas = get_schema_list(planList.required_table_names)

    # => I did followed the following steps to do the query: {queryList}    

    prompt = f"""I have a sql db with the following tables: {tables}
    => My goal is to do the following query: {query}
    => And Here are the required schemas of the tables: {schemas}
    => I did the following query:
     {queryList.steps[-1].sql_query}
    => But, I got this error while running the final query: {error_message}
    => please fix the query and return a query which is correct
     and also reaches the goal.
      One note if the query is about any specific company 
    first you need to take the CompanyId using this sample query: SELECT CompanyId from Security.AppClientCompany WHERE CompanyName LIKE '%name_of_company%'
    where name_of_company is the name of the company given in the user query for which you want to get the CompanyId for.
    """

    get_llm_logger().info("FIXING QUERY USING LLM")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a sql query fixer.
             You will be given a natural language query, a sql query for that and a
             error message while running the query. Fix the sql query by analyzing 
             the error message to reach the goal and return in the fixed query
             according to the response format ."""},
            {"role": "user", "content": prompt}
        ],
        response_format=FixQuery,
    )

    fixed_query = completion.choices[0].message.parsed.fixed_query

    get_llm_logger().info(f"FIXED QUERY FROM AI : {fixed_query}")

    return fixed_query, completion.usage.total_tokens
