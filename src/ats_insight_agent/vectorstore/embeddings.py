from loguru import logger
from src.ats_insight_agent.dto.resume_document import ResumeDocument
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ats_insight_agent.utils.Utility import Utility
from typing import List

class Embeddings:
    def __init__(self):
        self.utility = Utility()
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
            
            ## Clean resume content
            cleaned_content = self.utility.clean_resume_text(resume.content)
            logger.debug(f"Cleaned Resume Content: {cleaned_content}")
            
            ## Split resume content into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_text(cleaned_content)
            
            ### Generate embeddings
            # resume.vectors = self.generate_openai_embeddings(chunks)
            # resume.vectors = self.generate_huggingface_embeddings(chunks)
            # resume.vectors = self.generate_googleai_embeddings(chunks)
            resume.vectors = self.generate_fastembed_embeddings(chunks)
            
            chunk_rows = []
            for i, (chunk_text, vector) in enumerate(zip(chunks, resume.vectors)):
                chunk_id = f"{resume.doc_id}_{i}"
                row = {
                    "chunk_id": chunk_id,
                    "resume_id": resume.doc_id,
                    "filename": resume.filename,
                    "chunk_text": chunk_text,
                    "metadata": resume.metadata,
                    "chunk_vector": vector
                }
                chunk_rows.append(row)

            resume.chunks = chunk_rows
            logger.info(f"Generated vector for document: {resume.filename}")
            return resume
            
        except Exception as e:
            logger.error(f"Failed to generate vector for {resume.filename}: {str(e)}")
            raise
        
    
    def generate_openai_embeddings(self, content: List[str]):
        
        """Generate embeddings using OpenAI's model."""
        logger.info("Generating embeddings using OpenAI model")

        client = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=768
        )
        response = client.embed_documents(content)
        return response
        
    
    def generate_huggingface_embeddings(self, content: List[str]):
        """Generate embeddings using Hugging Face model."""
        
        logger.info("Generating embeddings using Hugging Face model")
        
        model = SentenceTransformer('ibm-granite/granite-embedding-278m-multilingual')
        vector = model.encode(content).tolist()
        return vector
    
    def generate_fastembed_embeddings(self, content: List[str]):
        """Generate embeddings using Fast Embed model."""
        
        logger.info("Generating embeddings using Fast Embed model")
        
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
        vector = embeddings.embed_documents(content)
        return vector

    def generate_googleai_embeddings(self, content: List[str]):
        
        """Generate embeddings using Google's model."""
        
        logger.info("Generating embeddings using Google model")
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"
        )
        response = embeddings.embed_documents(content)
        return response