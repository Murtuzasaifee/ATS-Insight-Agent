from pydantic import BaseModel, Field
from typing import List
import os
from loguru import logger
from src.ats_insight_agent.parser.docling_parser import DoclingParser
from src.ats_insight_agent.vectorstore.embeddings import Embeddings
from src.ats_insight_agent.vectorstore.milvus_store import MilvusStore
import json

class ResumeProcessorConfig(BaseModel):
    """Configuration for the resume processor."""
    collection_name: str = Field(default="resumes")
    collection_desc: str = Field(default="Resume collection")
    index_file_size: int = Field(default=32)
    vector_dim: int = Field(default=768)
    supported_extensions: List[str] = Field(default=[".pdf", ".docx", ".html"])
    

class ResumeProcessor:
    
    def __init__(self, llm):
        self.llm = llm
        self.config = ResumeProcessorConfig()
        self.docling_parser = DoclingParser(self.config.supported_extensions)
        self.embeedings = Embeddings()
        self.vector_store = MilvusStore(self.config.collection_name, self.config.collection_desc, self.config.vector_dim )
        self.vector_store.setup_collection()
       
        
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
        
        # Vectorize resume
        # resume = self.embeedings.vectorize_resume(resume)
        resume = self.embeedings.vectorize_resume(resume)
        
        # Store in Milvus
        doc_id = self.vector_store.store_resume(resume)
        
        return doc_id