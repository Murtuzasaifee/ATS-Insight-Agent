from pydantic import BaseModel, Field
from typing import List
import os
from loguru import logger
from src.ats_insight_agent.parser.docling_parser import DoclingParser
from src.ats_insight_agent.vectorstore.embeddings import Embeddings
from src.ats_insight_agent.vectorstore.milvus_store import MilvusStore
from src.ats_insight_agent.state.ats_state import ATSState
from src.ats_insight_agent.dto.config import Config
    

class ResumeProcessor:
    
    def __init__(self, llm, milvus_store:MilvusStore, config: Config):
        self.llm = llm
        self.config = config
        self.docling_parser = DoclingParser(self.config.supported_extensions)
        self.embeedings = Embeddings()
        self.vector_store = milvus_store
       
        
    def process_resume_file(self, state: ATSState) -> str:
        """
        Process a resume file: parse, vectorize, and store in Milvus.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Document ID of the stored resume
        """
        # Parse resume
        resume = self.docling_parser.parse_resume(state.file_path)
        logger.debug(f"Resume Content: {resume.model_dump_json()}")
        
        # Vectorize resume
        resume = self.embeedings.vectorize_resume(resume)
        
        # Store in Milvus
        resume_id = self.vector_store.store_chunks(resume.chunks)
        state.resume_id = resume_id
        return state