from loguru import logger
from src.ats_insight_agent.dto.resume_document import ResumeDocument
from openai import OpenAI

class Embeddings:
    def __init__(self):
        pass
        
    def vectorize_resume(self, resume: ResumeDocument) -> ResumeDocument:
        """
        Generate vector embeddings for the resume content.
        
        Args:
            resume: ResumeDocument object
            
        Returns:
            ResumeDocument with vector field populated
        """
        try:
            
            # Generate embeddings
            resume.vector = self.generate_openai_embeddings(resume.content)
            
            logger.info(f"Generated vector for document: {resume.filename}")
            return resume
            
        except Exception as e:
            logger.error(f"Failed to generate vector for {resume.filename}: {str(e)}")
            raise
        
    
    def generate_openai_embeddings(self, content: str):
        
        """Generate embeddings using OpenAI's model."""
        
        client = OpenAI()
        response = client.embeddings.create(
            input= content,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
        
        
