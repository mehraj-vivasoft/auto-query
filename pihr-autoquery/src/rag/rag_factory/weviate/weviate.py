from src.rag.rag_factory.rag_interface import RAGInterface
from typing import List, Any, Dict
import weaviate
import os
from dotenv import load_dotenv
from src.rag.rag_factory.weviate.helpers.post_chunk import post_chunk
from src.rag.rag_factory.weviate.helpers.get_all_chunks import get_chunks
from src.rag.rag_factory.weviate.helpers.get_top_k_chunks import get_top_k_chunks
from src.rag.rag_factory.weviate.helpers.get_chunks_by_id import get_chunks_by_id
from src.rag.rag_factory.weviate.helpers.get_collection_names import get_collection_names
from src.rag.rag_factory.weviate.helpers.delete_chunks_by_id import delete_chunks_by_id
from abc import abstractmethod


class WeviateDatabaseInistance(RAGInterface):
    
    client = None
    
    def __init__(self):
        self.connect()
    
    def connect(self) -> None:        
        load_dotenv()        
        client = weaviate.connect_to_local(headers={
            "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]
        })
        if client is None:
            raise Exception("Weaviate is not running")
        else:
            print("Weaviate is running")
        self.client = client
        return
    
    def disconnect(self) -> None:
        """Close database connection"""
        self.client.close()
        self.client = None
        print("Weaviate is closed")
        return
    
    def post_chunk(self, collection: str, data: List[Dict[str, str]]):
        """Post a document to the RAG"""
        if self.client is None:
            raise Exception("Weaviate is not running")
        post_chunk(collection, data, self.client)
        return
    
    def get_top_k_chunks(self, collection: str, query: str, top_k: int, is_simple: bool = False) -> List[Dict[str, str]]:
        """Get a response from the RAG"""
        if self.client is None:
            raise Exception("Weaviate is not running")        
        return get_top_k_chunks(collection, query, self.client, top_k, is_simple)
    
    def get_all_chunks(self, collection: str) -> List[Dict[str, str]]:
        """Get all responses from the RAG"""
        if self.client is None:
            raise Exception("Weaviate is not running")
        return get_chunks(collection, self.client)
    
    def get_chunks_by_ids(self, collection: str, ids: List[str]) -> List[Dict[str, str]]:
        """Get a response from the RAG"""
        if self.client is None:
            raise Exception("Weaviate is not running")
        return get_chunks_by_id(collection, ids, self.client)
    
    def get_collection_names(self) -> List[str]:
        """Get all table names from database"""
        if self.client is None:
            raise Exception("Weaviate is not running")
        return get_collection_names(self.client)

    def delete_chunks_by_id(self, collection: str, ids: List[str]) -> List[Any]:
        """Delete chunks by id"""
        if self.client is None:
            raise Exception("Weaviate is not running")
        return delete_chunks_by_id(collection, ids, self.client)