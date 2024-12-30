from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from src.chat.llm_factory.llm_interface import LLMInterface
from src.chat.schema import ChatRequest, NewConversationModel, MessageModel, ReplyModel
from src.chat.llm_factory.openai.openai import OpenAiLLM
from src.db.db_factory.db_interface import DBInterface
from src.db.db_factory.mongo.mongo import MongoDB
from dotenv import load_dotenv
import os

# Initialize FastAPI router
router = APIRouter()

# Dependency to ensure MongoDB is connected
def get_llm() -> LLMInterface:
    load_dotenv()
    llm_instance = OpenAiLLM(api_key=os.getenv("OPENAI_API_KEY"))        
    
    if not llm_instance:
        raise HTTPException(status_code=500, detail="LLM not connected")

    try:
        yield llm_instance
    finally:
        llm_instance = None

def get_db() -> DBInterface:
    db_instance = MongoDB(uri="mongodb://localhost:27017", db_name="chat_db")
    db_instance.connect()
    
    if not db_instance.db:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    try:
        yield db_instance
    finally:
        db_instance.disconnect()

@router.post("/", response_class=NewConversationModel | MessageModel)
async def complete_query(chat_init: ChatRequest, llm: LLMInterface = Depends(get_llm), db: DBInterface = Depends(get_db)):
    """
    Endpoint to generate a response based on previous messages.

    Args:
    - chat_init (ChatRequest): Contains user_id, conversation_id, and query

    Returns:
    - str: Contains the response
    """

    assistant_response = None
    validation_chk = llm.check_validation(chat_init.question)
    
    if validation_chk.is_safe:
        print("Safe to continue")
        assistant_response = await llm.generate_response(
            query=chat_init.question, user_id=chat_init.user_id, conversation_id=chat_init.conversation_id
        )
    else:
        print("Unsafe to continue")                
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
        print("New Conversation")        
        db.create_conversation(
            conversation_id=chat_init.conversation_id,
            title=chat_init.question,
            user_id=chat_init.user_id
        )        
        return NewConversationModel(conversation_id=chat_init.conversation_id, 
                                    user_id=chat_init.user_id,                                    
                                    subject=chat_init.question,
                                    reply=ReplyModel(message=assistant_response))
        
    else:
        print("Continuing Conversation")                
        return MessageModel(message_id=chat_document.message_id,
                            conversation_id=chat_document.conversation_id,
                            content=chat_document.message,
                            timestamp=chat_document.created_at)