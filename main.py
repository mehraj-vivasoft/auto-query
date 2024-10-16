from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.step_executor import step_executor
from core.query_planner import query_planner
from core.step_maker import step_maker
from db.database import connect_db, disconnect_db, execute_query, get_schema_list, get_table_names, get_table_schema
from utils.logging_config import get_app_logger, setup_logging
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class  SchemaRequest(BaseModel):
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

# --------------------------------  ROUTES  -------------------------------- #

@app.post("/items/")
async def read_items(query: ManualQuery):
    # query = "SELECT p.name FROM person p JOIN (SELECT c.courseid, ci.personid FROM course c JOIN courseinstructor ci ON c.courseid = ci.courseid JOIN department d ON c.departmentid = d.departmentid WHERE d.name = 'Mathematics') AS instructors ON p.personid = instructors.personid"
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
    return "Lets go!!"

@app.post("/query")
async def query_in_natural_language(request: QueryRequest):
    # planner: query -> plan
    plan = query_planner(request.query)
    # step maker: plan -> steps
    steps = step_maker(request.query, plan)
    # executor: steps -> results
    query_result = await step_executor(request.query, steps, plan)
    # if query_result.startswith("Error"):
    #     return query_result
    # results -> response
        
    return query_result
