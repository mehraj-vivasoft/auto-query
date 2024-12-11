import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

# from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

class ChartConfig(BaseModel):
    isBarChartPossible: bool


async def chart_maker(query: str, sql_query: str, output: str) -> ChartConfig:

    prompt = f"""The natural language query of the user is : {query}
    I am doing the following sql query for the user query: {sql_query}
    After executing the query in the database, the output is as follows: {output}
    Now you have to tell me if I can make a bar chart from the output of the query.    
    
    # Note:
    - Bar chart can be made only if the output can be presented in the form of key-value pairs and among which value is numeric
    
    # You should retrun the following response format:
    - isBarChartPossible: True, if a bar chart can be made from the output, False otherwise     
    """
    
    # get_llm_logger().info(f"Processing output of the query")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a dicision agent which can decide which type of graph can be made
             from a given query and output. I will provide you a natural language query, a sql query and the response snapshot 
             after executing the query in the database. Your task is find out which type of graph can be made from the output.
             You should retrun the following response format:
             - isBarChartPossible: True, if a bar chart can be made from the output, False otherwise
            """},
            {"role": "user", "content": prompt}
        ],
        response_format=ChartConfig,
    )

    chart_configaration = completion.choices[0].message.parsed
    usage = completion.usage.total_tokens

    # get_llm_logger().info(f"Bar Chart FROM AI : {bar_chart}")    

    return chart_configaration, usage

# if __name__ == "__main__":
#     import asyncio

#     async def main():
#         natural_lang = "give me the employee names and total leave days of last 3 months and sort them by total leave days count"
#         query = "[('Md', 'Ariful', 'Islam', Decimal('7.5')), ('Alim', 'Uddin', 'Rafi', Decimal('7.0')), ('Md. Ariful islam', None, 'Manik', Decimal('7.0')), ('Kawsar', 'Hossain', 'Eidul', Decimal('7.0')), ('Afraeem', None, 'Ahmed', Decimal('3.0')), ('S.M Shamiun', None, 'Noor', Decimal('2.0')), ('Md.Shoukut Akbar', None, 'Shuvo', Decimal('1.0')), ('Mehedi', 'Al', 'Masud', Decimal('1.0')), ('Shayekh', 'Ebne', 'Mizan', Decimal('1.0')), ('Jahid', 'Bin', 'Moshiur', Decimal('0.0')), ('Prodipta', None, 'sen', Decimal('0.0')), ('Jayakumar', '.', 'Jayaraman', Decimal('0.0')), ('PiHR2', None, 'QA1', Decimal('0.0')), ('Diganta', None, 'Das', Decimal('0.0')), ('Md. Abdullah AL', None, 'Kafi', Decimal('0.0')), ('Oahidul', None, 'Islam', Decimal('0.0')), ('Rajib Kumar', None, 'Saha', Decimal('0.0')), ('Biplab', None, 'Sarker', Decimal('0.0')), ('Ayesha', None, 'Siddique', Decimal('0.0')), ('Mohammad', 'Aminul', 'Islam', Decimal('0.0')), ('Sergio', None, 'Busquets', Decimal('0.0')), ('akbar', None, 'shouvo', Decimal('0.0')), ('Nahid', None, 'hossain', Decimal('0.0'))]"
#         sql_query = "SELECT e.FirstName, e.MiddleName, e.LastName, COALESCE(l.TotalLeaveDays, 0) AS TotalLeaveDays FROM Employee.Employee e LEFT JOIN (SELECT EmployeeId, SUM(DayCount) AS TotalLeaveDays FROM Leave.LeaveApplication WHERE CompanyId = 1 AND FromDate >= DATEADD(MONTH, -3, GETDATE()) GROUP BY EmployeeId) l ON e.EmployeeId = l.EmployeeId WHERE e.CompanyId = 1 ORDER BY TotalLeaveDays DESC;"
#         try:
#             chart_config = await chart_maker(natural_lang, sql_query, query)
#             print(chart_config)
#         except Exception as e:
#             print(e)
#         if chart_config.isBarChartPossible:
#             print("Bar Chart Possible")
#         else:
#             print("Bar Chart Not Possible")

#     asyncio.run(main())