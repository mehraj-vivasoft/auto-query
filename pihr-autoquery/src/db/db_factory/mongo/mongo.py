from pymongo import MongoClient
from typing import List, Any, Dict
from src.db.db_factory.db_interface import DBInterface

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

    def post_chat(self, thread_id: str, user_id: str, role: str, message: str, msg_summary: str) -> None:
        """Post a chat message to the database"""
        thread_collection = self.db["threads"]        
        if not thread_collection.find_one({"id": thread_id}):
            thread_document = {
                "id": thread_id,
                "title": thread_id,
                "user_id": user_id,
                "timestamp": self._get_current_timestamp()
            }
            thread_collection.insert_one(thread_document)
        chats_collection = self.db["chats"]
        chat_document = {
            "thread_id": thread_id,
            "user_id": user_id,
            "role": role,
            "message": message,
            "msg_summary": msg_summary,
            "timestamp": self._get_current_timestamp()
        }
        chats_collection.insert_one(chat_document)
        print(f"Chat posted to thread {thread_id}.")

    def get_chat_by_page(self, thread_id: str, page_number: int, page_size: int = 10) -> List[Dict[str, Any]]:
        """Get a list of chat threads and messages, sorted by the latest message's timestamp"""
        chats_collection = self.db["chats"]
        skip_count = (page_number - 1) * page_size
        chats = chats_collection.find({"thread_id": thread_id}).sort("timestamp", -1).skip(skip_count).limit(page_size)
        return list(chats)
    
    def get_chat_context(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get the recent 6 chats for a given thread id"""
        chats_collection = self.db["chats"]
        context = chats_collection.find({"thread_id": thread_id}).sort("timestamp", -1).limit(6)
        return list(context)
    
    def get_all_threads(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all threads of a user"""
        threads_collection = self.db["threads"]
        threads = threads_collection.find({"user_id": user_id})
        response = []
        for thread in threads:
            response.append({"thread": thread, "total_page": self._get_total_page(thread["thread_id"])})
        return response

    def _get_total_page(self, thread_id: str) -> int:
        """Get total number of page of a thread id"""
        chats_collection = self.db["chats"]
        total_count = chats_collection.count_documents({"thread_id": thread_id})        
        return (total_count + 9) // 10
    
    def _get_current_timestamp(self) -> str:
        """Helper method to get the current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()

# Example usage:
# mongo = MongoDB(uri="mongodb://localhost:27017", db_name="chat_db")
# mongo.connect()
# mongo.post_chat("thread123", "user456", "user", "Hello!", "Greeting message")
# chats = mongo.get_chat_by_page("thread123", 1)
# print(chats)
# context = mongo.get_chat_context("thread123")
# print(context)
# mongo.disconnect()
