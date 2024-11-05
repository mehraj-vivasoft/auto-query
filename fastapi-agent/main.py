from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from core.error_processsor import error_processor
from core.output_processor import output_processor
from core.step_executor import step_executor
from core.query_planner import query_planner, plan_list_to_str
from core.step_maker import step_maker, steps_to_str
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
import asyncio


class QueryRequest(BaseModel):
    query: str


class SchemaRequest(BaseModel):
    table_names: list[str]


class ManualQuery(BaseModel):
    query: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await connect_db()
    logger = get_app_logger()
    logger.info("Application started")
    yield
    await disconnect_db()
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
def read_items(query: ManualQuery):
    results = execute_query(query)
    return results


@app.get("/tables/")
def tables():
    return {"tables": get_table_names()}


@app.post("/schema")
def schema(request: SchemaRequest):
    tables = request.table_names
    return {"schema": get_schema_list(tables)}


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
    return StreamingResponse(streamer(request))


async def streamer(request: QueryRequest):
    
    logger = get_app_logger()    
    logger.info(f"Received query: {request.query}")    
    
    yield "received query"
    
    yield "Calling Table Selector agent"
    
    # table selector: query -> tables
    selected_tables = table_selector_from_query(request.query)
            
    yield "Selected Tables are: " + str(selected_tables)
    
    logger.info(f"Calling Query Planner agent")
    
    yield "Calling Query Planner agent"
    
    # planner: query -> plan
    plan = query_planner(request.query, selected_tables)
        
    yield "Created Plan is : " + str(plan)
    
    yield "Calling Step Maker agent"
    
    logger.info(f"Calling Step Maker agent")
    
    # step maker: plan -> steps
    steps = step_maker(request.query, plan, selected_tables)
    
    yield "Created Steps are : " + str(steps)
    
    yield "Calling Step Executor agent"
    
    logger.info(f"Calling Step Executor agent")
    
    # executor: steps -> results
    query_result = await step_executor(request.query, steps, plan, selected_tables)
    
        
    query_result_str = str(query_result)
    if query_result_str.startswith("Error"):
        logger.error(f"Error in query execution: {query_result}")
        yield "Error in query execution calling error processor agent"
        error_explaination = error_processor(request.query, query_result_str, steps.steps[len(steps.steps) - 1].sql_query)
        response = {
            "result": error_explaination,    
            "error": query_result_str,   
            "steps": convert_to_serializable(steps),
            "plan": convert_to_serializable(plan)
        }      
        yield "Error reason: " + str(error_explaination)
        
        yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
        
        yield str(response)
        
    
    yield "Query Executed successfully"
    
    yield "Query Result: " + str(query_result)
    
    yield "Calling Output Processor agent"
    
    logger.info(f"Calling Output Processor agent")
    
    # results -> llm response
    processed_output = output_processor(request.query, query_result)  
    
    yield "Output Processed: " + str(processed_output)
        
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
    
    yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
    
    yield str(response)
    
# async def streamer(request: QueryRequest):
    
#     logger = get_app_logger()    
#     logger.info(f"Received query: {request.query}")    
    
#     yield "{\"status\": \"Received query\"}"
    
#     yield "{\"status\": \"Calling Table Selector agent\"}"
    
#     # table selector: query -> tables
#     selected_tables = table_selector_from_query(request.query)
        
#     yield "{\"status\": \"Selected Tables\", \"content\": {\"tables\": " + str(selected_tables) + "}}"
    
#     logger.info(f"Calling Query Planner agent")
    
#     yield "{\"status\": \"Calling Query Planner agent\"}"
    
#     # planner: query -> plan
#     plan = query_planner(request.query, selected_tables)    
    
#     yield "{\"status\": \"Plan Created\", \"content\": {\"plan\": " + str(jsonable_encoder(plan)) + "}}"
    
#     yield "{\"status\": \"Calling Step Maker agent\"}\n\n"
    
#     logger.info(f"Calling Step Maker agent")
    
#     # step maker: plan -> steps
#     steps = step_maker(request.query, plan, selected_tables)
    
#     yield "{\"status\": \"Steps Created\", \"content\": {\"steps\": " + str(jsonable_encoder(steps)) + "}}"
    
#     yield "{\"status\": \"Calling Step Executor agent\"}"
    
#     logger.info(f"Calling Step Executor agent")
    
#     # executor: steps -> results
#     query_result = await step_executor(request.query, steps, plan, selected_tables)
    
        
#     query_result_str = str(query_result)
#     if query_result_str.startswith("Error"):
#         logger.error(f"Error in query execution: {query_result}")
#         yield "{\"status\": \"Error in query execution calling error processor agent\"}"        
#         error_explaination = error_processor(request.query, query_result_str, steps.steps[len(steps.steps) - 1].sql_query)
#         response = {
#             "result": error_explaination,    
#             "error": query_result_str,   
#             "steps": convert_to_serializable(steps),
#             "plan": convert_to_serializable(plan)
#         }      
#         yield "{\"status\": \"Error reason\", \"content\": {\"error\": \"" + str(error_explaination) + "\"}}"
        
#         yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
        
#         yield str(response)
        
    
#     yield "{\"status\": \"Query Executed\", \"content\": {\"query_result\": \"" + str(query_result) + "\"}}"
    
#     yield "{\"status\": \"Calling Output Processor agent\"}"
    
#     logger.info(f"Calling Output Processor agent")
    
#     # results -> llm response
#     processed_output = output_processor(request.query, query_result)  
    
#     yield "{\"status\": \"Output Processed\", \"content\": {\"processed_output\": \"" + str(processed_output) + "\"}}"
        
#     logger.info(f">>>>>>> Output Processor agent completed-----------------------------------")
#     logger.info(f"Result: {processed_output}")
#     logger.info(f"Query Result: {query_result}")
#     logger.info(f"Steps: {steps}")
#     logger.info(f"Plan: {plan}")  
    
#     response = {
#         "result": processed_output,    
#         "QueryResult": query_result_str,   
#         "steps": convert_to_serializable(steps),
#         "plan": convert_to_serializable(plan)
#     }  
    
#     yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
    
#     yield str(response)  