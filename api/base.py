# api/base.py

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/query")
async def search(request: SearchRequest):    

    return {"query": request.query}