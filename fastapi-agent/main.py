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
from core.bouncer import bouncer
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

@app.get("/companies")
def companies():
    results = execute_query("SELECT CompanyId, CompanyName FROM Security.AppClientCompany;")
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
    return StreamingResponse(streamer(request))


async def streamer(request: QueryRequest):
    
    total_tokens = 0
    
    logger = get_app_logger()    
    logger.info(f"Received query: {request.query}")    
    
    yield "<<GGWWP>>QUERY RECEIVED"
    
    yield "<<GGWWP>>DOING SAFETY CHECK... "
    
    safe_check, safe_check_tokens = bouncer(request.query)
    total_tokens += safe_check_tokens
    
    if safe_check.isSafe == False:                
        
        reason = str(safe_check.reasoningForSafetyOrDanger)
        
        yield "<<GGWWP>>QUERY IS NOT SAFE<<GGWWP>>" + reason
        
        yield "<<GGWWP>>TOTAL TOKENS USED: " + str(total_tokens)
        
        await asyncio.sleep(2)        
        
        yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
        
        
        return
    
    yield "<<GGWWP>>CALLING TABLE SELECTOR AGENT"
    
    # table selector: query -> tables
    selected_tables, selected_tables_token = table_selector_from_query(request.query)
    
    total_tokens += selected_tables_token
            
    yield "<<GGWWP>>Selected Tables are: " + str(selected_tables)
    
    logger.info(f"Calling Query Planner agent")
    
    yield "<<GGWWP>>CALLING QUERY PLANNER AGENT"
    
    # planner: query -> plan
    plan, plan_token = query_planner(request.query, selected_tables)
    
    total_tokens += plan_token
        
    yield "<<GGWWP>>Created Plan is : " + str(plan.model_dump_json())
    
    
    yield "<<GGWWP>>CALLING STEP MAKER AGENT"
    logger.info(f"Calling Step Maker agent")
    
    # step maker: plan -> steps
    steps, steps_token = step_maker(request.query, plan, selected_tables)
    
    total_tokens += steps_token
    
    yield "<<GGWWP>>Created Steps are : " + str(steps.model_dump_json())
    
    yield "<<GGWWP>>CALLING STEP EXECUTOR AGENT"
    
    logger.info(f"Calling Step Executor agent")
    
    # executor: steps -> results
    query_result, query_result_token = await step_executor(request.query, steps, plan, selected_tables)
    
    total_tokens += query_result_token
        
    query_result_str = str(query_result)
    if query_result_str.startswith("Error"):
        logger.error(f"Error in query execution: {query_result}")
        yield "<<GGWWP>>ERROR IN QUERY EXECUTION - CALLING ERROR PROCESSOR AGENT"
        error_explaination, error_processor_token = error_processor(request.query, query_result_str, steps.steps[len(steps.steps) - 1].sql_query)        
        total_tokens += error_processor_token
        response = {
            "result": error_explaination,    
            "error": query_result_str,   
            "steps": convert_to_serializable(steps),
            "plan": convert_to_serializable(plan)
        }      
        yield "<<GGWWP>>ERROR REASON: " + str(error_explaination)
        
        yield "<<GGWWP>>TOTAL TOKENS USED: " + str(total_tokens)
        
        await asyncio.sleep(3)
        
        yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
        
        return
        
        # return str(response)
        
    
    yield "<<GGWWP>>QUERY EXECUTED SUCCESSFULLY"
    
    yield "<<GGWWP>>Query Result: " + str(query_result)
    
    yield "<<GGWWP>>CALLING OUTPUT PROCESSOR AGENT"
    
    logger.info(f"Calling Output Processor agent")
    
    # results -> llm response
    processed_output, processed_output_token = output_processor(request.query, query_result)  
    
    total_tokens += processed_output_token
    
    yield "<<GGWWP>>Output Processed: " + str(processed_output)
        
    logger.info(f">>>>>>> Output Processor agent completed-----------------------------------")
    logger.info(f"Result: {processed_output}")
    logger.info(f"Query Result: {query_result}")
    logger.info(f"Steps: {steps}")
    logger.info(f"Plan: {plan}")  
    
    # response = {
    #     "result": processed_output,    
    #     "QueryResult": query_result_str,   
    #     "steps": convert_to_serializable(steps),
    #     "plan": convert_to_serializable(plan)
    # }  
    
    yield "<<GGWWP>>TOTAL TOKENS USED: " + str(total_tokens)
    
    await asyncio.sleep(3)
    
    yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
    
    # return response
