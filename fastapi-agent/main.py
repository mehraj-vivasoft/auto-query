from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from core.error_processsor import error_processor
from core.output_processor import output_processor
from core.step_executor import step_executor
from core.query_planner import query_planner
from core.step_maker import step_maker
from core.table_finder.table_selector_from_query import table_selector_from_query
from db.get_schema_list import get_schema_list
from db.database import (
    connect_db, disconnect_db, execute_query,
    get_table_names
)
from utils.logging_config import get_app_logger, setup_logging
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from streamer import streamer
from db_factory.db_providers.mssql import MSSQLDatabaseInistance
from db_factory.db_providers.sqlite import SQLiteDatabaseInstance

class QueryRequest(BaseModel):
    query: str


class SchemaRequest(BaseModel):
    table_names: list[str]


class ManualQuery(BaseModel):
    query: str


# db_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    global db_instance
    db_instance = MSSQLDatabaseInistance()
    # db_instance = SQLiteDatabaseInstance()
    await db_instance.connect()
    logger = get_app_logger()
    logger.info("Application started")
    yield
    await db_instance.disconnect()
    logger.info("Application stopped")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------  ROUTES  -------------------------------- #

@app.post("/items/")
def read_items(req: ManualQuery):    
    print(req.query)
    results = db_instance.execute_query(req.query)
    return str(results)

@app.get("/tables/")
def tables():
    return {"tables": db_instance.get_table_names()}

@app.post("/schema")
def schema(request: SchemaRequest): 
    tables = request.table_names
    return {"schema": db_instance.get_schema_list(tables)}

@app.get("/")
def read_root():
    # table_selector_from_query("Who are the most absent employees?")
    return "Lets go!!"

def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        return convert_to_serializable(vars(obj))
    else:
        return obj
    
@app.get("/companies")
def companies():
    results = db_instance.execute_query("SELECT CompanyId, CompanyName FROM Security.AppClientCompany;")
    formatted_results = [{"id": id, "name": name} for id, name in results]
    results = formatted_results
    print(results)
    return convert_to_serializable(results)

@app.post("/query")
async def query_in_natural_language(request: QueryRequest):
    
    logger = get_app_logger()    
    logger.info(f"Received query: {request.query}")    
    
    # table selector: query -> tables
    selected_tables = table_selector_from_query(request.query)        
    
    logger.info(f"Calling Query Planner agent")
    
    # planner: query -> plan
    plan = query_planner(request.query, selected_tables)
    
    logger.info(f"Calling Step Maker agent")
    
    # step maker: plan -> steps
    steps = step_maker(request.query, plan, selected_tables)
    
    logger.info(f"Calling Step Executor agent")
    
    # executor: steps -> results
    query_result = await step_executor(request.query, steps, plan, selected_tables)
    
    query_result_str = str(query_result)
    if query_result_str.startswith("Error"):
        logger.error(f"Error in query execution: {query_result}")
        error_explaination = error_processor(request.query, query_result_str, steps.steps[len(steps.steps) - 1].sql_query)
        response = {
            "result": error_explaination,    
            "error": query_result_str,   
            "steps": convert_to_serializable(steps),
            "plan": convert_to_serializable(plan)
        }      
        return JSONResponse(status_code=500, content=response)
    
    logger.info(f"Calling Output Processor agent")
    
    # results -> llm response
    processed_output = output_processor(request.query, query_result)  
        
    logger.info(f">>>>>>> Output Processor agent completed-----------------------------------")
    logger.info(f"Result: {processed_output}")
    logger.info(f"Query Result: {query_result}")
    logger.info(f"Steps: {steps}")
    logger.info(f"Plan: {plan}")  
    
    response = {
        "result": processed_output,    
        "QueryResult": query_result_str,   
        "steps": convert_to_serializable(steps),
        "plan": convert_to_serializable(plan)
    }  
    
    # return query_result
    return response

@app.post("/query/stream")
async def stream_query_in_natural_language(request: QueryRequest):        
    
    # return query_result
    return StreamingResponse(streamer(request, db_instance), media_type="text/event-stream")
