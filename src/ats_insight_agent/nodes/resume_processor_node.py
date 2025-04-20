from pydantic import BaseModel, Field
from typing import List
import os
from loguru import logger
from src.ats_insight_agent.parser.docling_parser import DoclingParser
import json

class ResumeProcessorConfig(BaseModel):
    """Configuration for the resume processor."""
    collection_name: str = Field(default="resumes")
    vector_dim: int = Field(default=768)
    index_file_size: int = Field(default=32)
    supported_extensions: List[str] = Field(default=[".pdf", ".docx", ".html"])
    

class ResumeProcessor:
    
    def __init__(self, llm):
        self.llm = llm
        self.config = ResumeProcessorConfig()
        self.docling_parser = DoclingParser(self.config.supported_extensions)
       
        
    def process_resume_file(self, file_path: str) -> str:
        """
        Process a resume file: parse, vectorize, and store in Milvus.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Document ID of the stored resume
        """
        # Parse resume
        resume = self.docling_parser.parse_resume(file_path)
        logger.debug(f"Resume Content: {resume.model_dump_json()}")
        
        # # Vectorize resume
        # resume = self.vectorize_resume(resume)
        
        # # Store in Milvus
        # doc_id = self.store_resume(resume)
        
        # return doc_id