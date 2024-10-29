from contextlib import asynccontextmanager
from fastapi import FastAPI
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
async def read_items(query: ManualQuery):
    results = await execute_query(query)
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


@app.post("/query")
async def query_in_natural_language(request: QueryRequest):
    
    # table selector: query -> tables
    selected_tables = table_selector_from_query(request.query)
    
    # planner: query -> plan
    plan = query_planner(request.query, selected_tables)
    
    # step maker: plan -> steps
    steps = step_maker(request.query, plan, selected_tables)
    
    # executor: steps -> results
    query_result = await step_executor(request.query, steps, plan)
    
    if query_result.startswith("Error"):
        return query_result
    
    # results -> llm response
    processed_output = output_processor(request.query, query_result)  
    
    # return query_result
    return {"result": processed_output, "query_result": query_result, "steps": steps, "plan": plan, }
