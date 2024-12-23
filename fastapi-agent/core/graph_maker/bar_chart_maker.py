import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

# from utils.logging_config import get_llm_logger

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

class Bar(BaseModel):
    keyName: str
    value: int

class BarChart(BaseModel):
    bars: list[Bar]
    key_title: str
    value_title: str
    bar_chart_title: str
    bar_chart_description: str


async def bar_chart_maker(query: str, output: str) -> BarChart:

    prompt = f"""The natural language query of the user is : {query}
    After executing the query in the database, the output is as follows:
    {output}
    Now you have to process the output of the query and format the output in Bar Chart format.
    The Bar Chart format should be as follows:
    bar_chart_title: The title of the bar chart
    bar_chart_description: The description of the bar chart
    key_title: The title of the key
    value_title: The title of the value
    bars: The bars of the bar chart where each bar is as follows:
        keyName: The name of the key
        value: The value of the key
    """
    
    # get_llm_logger().info(f"Processing output of the query")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a bar chart maker.
            I will provide you a natural language query and the response after executing the query in the database.
            Your task is to process the output of the query and Give the response of the user query in Bar Chart format.
            The Bar Chart format should be as follows:
            bar_chart_title: The title of the bar chart
            bar_chart_description: The description of the bar chart
            key_title: The title of the key
            value_title: The title of the value
            bars: The bars of the bar chart where each bar is as follows:
                keyName: The name of the key
                value: The value of the key
            """},
            {"role": "user", "content": prompt}
        ],
        response_format=BarChart,
    )

    bar_chart = completion.choices[0].message.parsed

    # get_llm_logger().info(f"Bar Chart FROM AI : {bar_chart}")    

    return bar_chart.model_dump_json(), completion.usage.total_tokens

# if __name__ == "__main__":
#     natural_lang = "give me the employee names and total leave days of last 3 months and sort them by total leave days count"
#     query = "[('Md', 'Ariful', 'Islam', Decimal('7.5')), ('Alim', 'Uddin', 'Rafi', Decimal('7.0')), ('Md. Ariful islam', None, 'Manik', Decimal('7.0')), ('Kawsar', 'Hossain', 'Eidul', Decimal('7.0')), ('Afraeem', None, 'Ahmed', Decimal('3.0')), ('S.M Shamiun', None, 'Noor', Decimal('2.0')), ('Md.Shoukut Akbar', None, 'Shuvo', Decimal('1.0')), ('Mehedi', 'Al', 'Masud', Decimal('1.0')), ('Shayekh', 'Ebne', 'Mizan', Decimal('1.0')), ('Jahid', 'Bin', 'Moshiur', Decimal('0.0')), ('Prodipta', None, 'sen', Decimal('0.0')), ('Jayakumar', '.', 'Jayaraman', Decimal('0.0')), ('PiHR2', None, 'QA1', Decimal('0.0')), ('Diganta', None, 'Das', Decimal('0.0')), ('Md. Abdullah AL', None, 'Kafi', Decimal('0.0')), ('Oahidul', None, 'Islam', Decimal('0.0')), ('Rajib Kumar', None, 'Saha', Decimal('0.0')), ('Biplab', None, 'Sarker', Decimal('0.0')), ('Ayesha', None, 'Siddique', Decimal('0.0')), ('Mohammad', 'Aminul', 'Islam', Decimal('0.0')), ('Sergio', None, 'Busquets', Decimal('0.0')), ('akbar', None, 'shouvo', Decimal('0.0')), ('Nahid', None, 'hossain', Decimal('0.0'))]"
#     print(bar_chart_maker(natural_lang,query))