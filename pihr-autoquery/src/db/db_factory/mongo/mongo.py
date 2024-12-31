from pymongo import MongoClient
from typing import List, Any, Dict
from src.db.db_factory.db_interface import DBInterface
from datetime import datetime
from src.db.schemas import ChatMessageModel, AllConversationsResponseModel, MetadataModel, MessageModel, MessagesResponseModel

class MongoDB(DBInterface):
    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB connection parameters"""
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self) -> None:
        """Establish database connection"""
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        print(f"Connected to MongoDB database: {self.db_name}")

    def disconnect(self) -> None:
        """Close database connection"""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    def create_conversation(self, conversation_id: str, subject: str, user_id: str) -> AllConversationsResponseModel:
        """Create a new conversation in the database"""
        conversations_collection = self.db["conversations"]
        if not conversations_collection.find_one({"id": conversation_id}):
            current_timestamp = self._get_current_timestamp()
            conversation_document = {
                "id": conversation_id,
                "subject": subject,
                "user_id": user_id,
                "created_at": current_timestamp,
                "updated_at": current_timestamp
            }
            conversations_collection.insert_one(conversation_document)
            print(f"Conversation {conversation_id} created.")

    async def post_chat(self, conversation_id: str, user_id: str, role: str, message: str, msg_summary: str) -> ChatMessageModel:
        """Post a chat message to the database"""      
        chats_collection = self.db["chats"]
        current_timestamp = self._get_current_timestamp()
        chat_document = {            
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": role,
            "message": message,
            "msg_summary": msg_summary,
            "created_at": current_timestamp,
            "updated_at": current_timestamp
        }
        result = chats_collection.insert_one(chat_document)
        chat_document["message_id"] = result.inserted_id
        print(f"Chat posted to conversation {conversation_id}.")
        return ChatMessageModel(
            message_id=str(result.inserted_id),
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            message=message,
            msg_summary=msg_summary,
            created_at=current_timestamp,
            updated_at=current_timestamp
        )

    def get_chat_by_page(self, conversation_id: str, page_number: int, limit: int) -> MessagesResponseModel:
        """Get a list of chat conversations and messages, sorted by the latest message's timestamp"""
        chats_collection = self.db["chats"]
        skip_count = (page_number - 1) * limit
        chats = chats_collection.find({"conversation_id": conversation_id}).sort("timestamp", -1).skip(skip_count).limit(limit)
        chat_list = []
        for chat in chats:
            chat_list.append(MessageModel(id=str(chat["_id"]), 
                                          content=chat["message"], 
                                          role=chat["role"], 
                                          timestamp=chat["created_at"]))
        total_pages, total_entries = self._get_total_page(conversation_id=conversation_id, page_size=limit)
        return MessagesResponseModel(messages=chat_list, 
                                     metadata=MetadataModel(total=total_entries, 
                                                            page_number=page_number, 
                                                            total_pages=total_pages, 
                                                            page_size=limit))
    
    def get_chat_context(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get the recent 6 chats for a given conversation id"""
        chats_collection = self.db["chats"]
        context = chats_collection.find({"conversation_id": conversation_id}).sort("timestamp", -1).limit(6)
        return list(context)
    
    def get_all_conversations(self, user_id: str, page_number: int = 1, page_size: int = 10) -> AllConversationsResponseModel:
        """Get all conversations of a user"""
        conversations_collection = self.db["conversations"]
        total_pages, total_entries = self._get_total_page_overall(user_id=user_id, page_size=page_size)
        skip_count = (page_number - 1) * page_size
        conversations = conversations_collection.find({"user_id": user_id}).skip(skip_count).limit(page_size)
        response = []
        for conversation in conversations:
            response.append({
                "id": conversation["id"],
                "employee_id": conversation["user_id"],
                "subject": conversation["subject"],
                "created_at": conversation["created_at"],
                "updated_at": conversation["updated_at"]
            })                
        
        return AllConversationsResponseModel(conversations=response, 
                                             metadata=MetadataModel(total=total_entries, 
                                                                    page_number=page_number, 
                                                                    total_pages=total_pages, 
                                                                    page_size=page_size))
    
    def _get_total_page(self, conversation_id: str, page_size: int) -> (int, int):
        """Get total number of page of a conversation id"""
        chats_collection = self.db["chats"]
        total_count = chats_collection.count_documents({"conversation_id": conversation_id})        
        return ((total_count + page_size - 1) // page_size, total_count)

    def _get_total_page_overall(self, user_id: str, page_size: int) -> (int, int):
        """Get total number of page of a conversation id"""
        conversations_collection = self.db["conversations"]
        total_count = conversations_collection.count_documents({"user_id": user_id})
        return ((total_count + page_size - 1) // page_size, total_count)

    def _get_current_timestamp(self) -> str:
        """Helper method to get the current timestamp in ISO format with Z"""
        return datetime.now().isoformat() + "Z"


# Example usage:
# mongo = MongoDB(uri="mongodb://localhost:27017", db_name="chat_db")
# mongo.connect()
# mongo.post_chat("conversation123", "user456", "user", "Hello!", "Greeting message")
# chats = mongo.get_chat_by_page("conversation123", 1)
# print(chats)
# context = mongo.get_chat_context("conversation123")
# print(context)
# mongo.disconnect()
