import os
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, model=None, api_key=None):
        self.model = model
        self.api_key = api_key
        
        
    def get_llm_model(self):
        try:
            
            llm = ChatGroq(api_key=self.api_key,model=self.model)
        
        except Exception as e:
            raise ValueError(f"Error occured with Exception : {e}")
        
        return llm