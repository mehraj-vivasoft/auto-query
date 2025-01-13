from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Union
from src.chat.llm_factory.llm_interface import LLMInterface
from src.chat.schema import ChatRequest, NewConversationModel, MessageModel, ReplyModel
from src.chat.llm_factory.openai.openai import OpenAiLLM
from src.db.db_factory.db_interface import DBInterface
from src.db.db_factory.mongo.mongo import MongoDB
from dotenv import load_dotenv
import os

# Initialize FastAPI router
router = APIRouter()

async def get_llm() -> LLMInterface:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="Missing OpenAI API key")

    llm_instance = OpenAiLLM(api_key=api_key)

    try:
        print("Connected to LLM")
        yield llm_instance
    finally:
        # Perform cleanup if needed
        llm_instance = None

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

@router.post("/", response_model=Union[NewConversationModel, MessageModel])
async def complete_query(chat_init: ChatRequest, llm: LLMInterface = Depends(get_llm), db: DBInterface = Depends(get_db)):
    """
    Endpoint to generate a response based on previous messages.

    Args:
    - chat_init (ChatRequest): Contains user_id, conversation_id, and query

    Returns:
    - str: Contains the response
    """    
    
    assistant_response = None
    validation_chk = await llm.check_validation(chat_init.question)        
    
    if validation_chk.is_safe:        
        assistant_response = await llm.generate_response(
            query=chat_init.question, user_id=chat_init.user_id, conversation_id=chat_init.conversation_id
        )                        
    else:        
        assistant_response = validation_chk.reasoning_for_safety_or_danger
        
    await db.post_chat(
        conversation_id=chat_init.conversation_id,
        user_id=chat_init.user_id,
        role="user",
        message=chat_init.question,
        msg_summary=chat_init.question
    )
    
    chat_document = await db.post_chat(
        conversation_id=chat_init.conversation_id,
        user_id=chat_init.user_id,
        role="assistant",
        message=assistant_response,
        msg_summary=assistant_response
    )
    
    if chat_init.is_new:        
        db.create_conversation(
            conversation_id=chat_init.conversation_id,
            subject=chat_init.question,
            user_id=chat_init.user_id
        )        
        return NewConversationModel(conversation_id=chat_init.conversation_id, 
                                    user_id=chat_init.user_id,
                                    subject=chat_init.question,
                                    created_at=chat_document.created_at,
                                    updated_at=chat_document.updated_at,
                                    reply=ReplyModel(
                                        id=chat_document.message_id,
                                        content=assistant_response,
                                        timestamp=chat_document.created_at
                                    ))
        
    else:
        print("Continuing Conversation")                
        return MessageModel(message_id=chat_document.message_id,
                            conversation_id=chat_document.conversation_id,
                            content=chat_document.message,
                            timestamp=chat_document.created_at)