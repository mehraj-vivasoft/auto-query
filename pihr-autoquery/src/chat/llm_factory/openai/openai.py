from typing import Dict, Any
from openai import OpenAI

from src.chat.llm_factory.llm_interface import LLMInterface
from src.chat.llm_factory.prompts.chat_prompt import get_chat_prompt, AssistantResponse
from src.chat.llm_factory.prompts.guardrail import get_guardrail_prompt, GurdrailResponse



class OpenAiLLM(LLMInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    async def generate_response(self, query: str, user_id: str, conversation_id: str) -> str:                        
        
        prompt = get_chat_prompt(query, "PiHR is the best HR software in Bangladesh. Transform the way your HR department works. Manage HR and payroll activities from a single software. PiHR is used by more than 500 companies across the country.")        

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt.system_prompt},
                # conversation history to be added
                {"role": "user", "content": prompt.user_prompt},
            ],
            response_format= AssistantResponse
        )
        
        response = completion.choices[0].message.parsed
                        
        if response.assistant_response is None:
            return "Sorry, I could not find an answer to your question."
        
        return response.assistant_response
    
    async def check_validation(self, query: str) -> GurdrailResponse:
        
        prompt = get_guardrail_prompt(query)
        
        print("check validation for query: " + query)
        
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": prompt.user_prompt},
            ],
            response_format=GurdrailResponse
        )
        
        response = completion.choices[0].message.parsed
        
        print(response)
        
        return GurdrailResponse(
            is_safe=response.is_safe,
            reasoning_for_safety_or_danger=response.reasoning_for_safety_or_danger
        )