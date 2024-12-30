from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from src.db.db_factory.db_interface import DBInterface
from src.db.db_factory.mongo.mongo import MongoDB

# Initialize FastAPI router
router = APIRouter()

# Models
class ChatPost(BaseModel):
    thread_id: str
    user_id: str
    role: str
    message: str
    msg_summary: str

class ChatQuery(BaseModel):
    thread_id: str
    page_number: int
    page_size: int = 10

# Dependency to ensure MongoDB is connected
def get_db() -> DBInterface:
    db_instance = MongoDB(uri="mongodb://localhost:27017", db_name="chat_db")
    db_instance.connect()
    
    if not db_instance.db:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    try:
        yield db_instance
    finally:
        db_instance.disconnect()        

# Routes
@router.post("/chats", response_model=dict)
async def post_chat(chat: ChatPost, db: DBInterface = Depends(get_db)):
    """Endpoint to post a chat message."""
    try:
        db.post_chat(
            thread_id=chat.thread_id,
            user_id=chat.user_id,
            role=chat.role,
            message=chat.message,
            msg_summary=chat.msg_summary
        )
        return {"message": "Chat posted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post chat: {e}")

@router.get("/chats", response_model=List[Dict[str, Any]])
async def get_chats(thread_id: str, page_number: int = 1, page_size: int = 10, db: DBInterface = Depends(get_db)):
    """Endpoint to get chats by page."""
    try:
        chats = db.get_chat_by_page(thread_id, page_number, page_size)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chats: {e}")

@router.get("/chat-context", response_model=List[Dict[str, Any]])
async def get_chat_context(thread_id: str, db: DBInterface = Depends(get_db)):
    """Endpoint to get the last 6 chats for a thread."""
    try:
        context = db.get_chat_context(thread_id)
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chat context: {e}")
