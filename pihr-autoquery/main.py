from contextlib import asynccontextmanager
from fastapi import FastAPI

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.rag.routes import router as rag_router
from src.chat.routes import router as chat_router
from src.db.routes import router as db_router


version = "v1"

app = FastAPI()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
    # setup_logging()
    # global db_instance
    # db_instance = MSSQLDatabaseInistance()
    # db_instance = SQLiteDatabaseInstance()
    # await db_instance.connect()
    # logger = get_app_logger()    
    # logger.info("Application started")    
    # print("Application started")
    # yield
    # await db_instance.disconnect()
    # logger.info("Application stopped")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------  ROUTES  -------------------------------- #

@app.get("/")
async def root():
    return "PiHR X AutoQuery is Running"

app.include_router(rag_router, prefix=f"/api/{version}/rag", tags=['rag'])
app.include_router(db_router, prefix=f"/api/{version}/conversations", tags=['conversations'])
app.include_router(chat_router, prefix=f"/api/{version}/chats", tags=['chat'])
