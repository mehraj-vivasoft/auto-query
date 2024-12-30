from pydantic import BaseModel
from typing import List

class SingleRagEntry(BaseModel):
    document: str
    document_type: str
    tag: List[str]    
    
class SimpleRagEntryRequest(BaseModel):
    collection_name: str
    entries: list[SingleRagEntry]

class SimpleRagEntryResponse(BaseModel):
    message: str
    entries: list[SingleRagEntry]