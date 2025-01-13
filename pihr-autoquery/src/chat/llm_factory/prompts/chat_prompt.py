
# from user query, rag context of the query, and chat history: generate chat prompt
from typing import Any

from pydantic import BaseModel

class AssistantResponse(BaseModel):
    assistant_response: str
    assistant_response_summary: str

class Prompt(BaseModel):
    system_prompt: str
    user_prompt: str    

def get_chat_prompt(query: str, rag_context: str) -> Prompt:
    
    system_prompt = f"""
    You are a chatbot that answers questions about PiHR, which is a SaaS based fully integrated HR and payroll software management system and 
    user can ask for any information from PiHR Service and how to use it. Now, you have to answer the user query based on the RAG context and chat history.
    """
    
    user_prompt = f"""
    Here is the user query:
    User Query: {query}
    
    Here is some background information related to the user query:
    Background Context: {rag_context}            
    
    use the relevant information from the background context and ignore the irrelevant information from the background context to answer the user query.
    If you cannot answer the user query based on the background context, you should tell the user that you cannot answer the user query.
    
    Make sure that the response is not too long.
    
    Now you have to answer the user query based on the Background context and chat history.
    Response Format:
    - Assistant Response
    - Assistant Response Summary
    """
    
    return Prompt(system_prompt=system_prompt, user_prompt=user_prompt)