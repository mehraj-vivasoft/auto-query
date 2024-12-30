from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class ChatPost(BaseModel):
    conversation_id: str
    user_id: str
    role: str
    message: str
    msg_summary: str

class ChatQuery(BaseModel):
    conversation_id: str
    page_number: int
    
class ChatMessageModel(BaseModel):
    message_id: str
    conversation_id: str
    user_id: str
    role: str
    message: str
    msg_summary: str
    created_at: datetime
    updated_at: datetime
    
class ConversationModel(BaseModel):
    id: str
    employee_id: str
    subject: str
    created_at: datetime
    updated_at: datetime

class MetadataModel(BaseModel):
    total: Optional[int] = Field(None, description="Total number of entries")
    page_number: int
    total_pages: int
    page_size: int

class AllConversationsResponseModel(BaseModel):
    conversations: List[ConversationModel]
    metadata: MetadataModel
    
class MessageModel(BaseModel):
    id: str
    content: str
    role: str
    timestamp: datetime

class MessagesResponseModel(BaseModel):
    messages: List[MessageModel]
    metadata: MetadataModel