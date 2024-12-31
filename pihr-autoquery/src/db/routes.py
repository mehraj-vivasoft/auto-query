from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from src.db.db_factory.db_interface import DBInterface
from src.db.db_factory.mongo.mongo import MongoDB
from src.db.schemas import ChatPost, ChatQuery

# Initialize FastAPI router
router = APIRouter()

# Dependency to ensure MongoDB is connected
async def get_db() -> DBInterface:
    """Dependency to ensure MongoDB is connected with proper error handling."""
    db_instance = None
    try:
        db_instance = MongoDB(uri="mongodb://admin:kothinAdminPass@localhost:27017", db_name="chat_db")
        db_instance.connect()
        
        if db_instance.db is None:
            raise HTTPException(
                status_code=503, 
                detail="Database connection not available"
            )
            
        yield db_instance
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection error: {str(e)}"
        )
    finally:
        if db_instance:
            db_instance.disconnect()      

# Example API call: GET /conversations?user_id=<user_id>
@router.get("/", response_model=Any)
async def get_conversations(user_id: str, db: DBInterface = Depends(get_db)):
    """Endpoint to get all conversations for a user."""
    try:        
        conversations = db.get_all_conversations(user_id)
        print(conversations)
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversations: {e}")
    
# Example API call: GET /<conversation_id>?page=<page>&limit=<limit>
@router.get("/{conversation_id}", response_model=Any)
async def get_chats(conversation_id: str, page: int = 1, limit: int = 10, db: DBInterface = Depends(get_db)):
    """Endpoint to get chats by page."""
    try:        
        chats = db.get_chat_by_page(conversation_id, page, limit)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chats: {e}")

# Example API call: POST /chats
@router.post("/chats", response_model=dict)
async def post_chat(chat: ChatPost, db: DBInterface = Depends(get_db)):
    """Endpoint to post a chat message."""
    try:
        db.post_chat(
            conversation_id=chat.conversation_id,
            user_id=chat.user_id,
            role=chat.role,
            message=chat.message,
            msg_summary=chat.msg_summary
        )
        return {"message": "Chat posted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post chat: {e}")

@router.get("/chat-context", response_model=List[Dict[str, Any]])
async def get_chat_context(conversation_id: str, db: DBInterface = Depends(get_db)):
    """Endpoint to get the last 6 chats for a conversation."""
    try:
        context = db.get_chat_context(conversation_id)
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chat context: {e}")
