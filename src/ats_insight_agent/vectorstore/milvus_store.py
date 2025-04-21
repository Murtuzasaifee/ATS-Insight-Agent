from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from loguru import logger
from src.ats_insight_agent.dto.resume_document import ResumeDocument

class MilvusStore:
    
    def __init__(self, collection_name, collection_desc):
        
        self.collection_name = collection_name
        self.collection_desc = collection_desc
        self.host = "localhost"
        self.port = "19530"
        self.vector_dim =1536
        
        try:
            connections.connect(
                alias='default', 
                host= self.host, 
                port= int(self.port)
            )
            logger.info(f"Connected to Milvus at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {str(e)}")
            raise
        
    
    def setup_collection(self) -> None:
        """Set up the Milvus collection for storing resume vectors."""
        try:
            # Check if collection exists
            if utility.has_collection(self.collection_name):
                logger.info(f"Collection {self.collection_name} already exists")
                return
            
            # Define fields for the collection
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
                FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=256),
                FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=512),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="metadata", dtype=DataType.JSON),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.vector_dim)
            ]
            
            # Create schema and collection
            schema = CollectionSchema(fields=fields, description=self.collection_desc)
            collection = Collection(name=self.collection_name, schema=schema)
            
            # Create index on vector field
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            collection.create_index(field_name="vector", index_params=index_params)
            collection.load()
            logger.info(f"Created and indexed collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to set up collection: {str(e)}")
            raise
    
    def store_resume(self, resume: ResumeDocument) -> str:
        """
        Store a resume document in the Milvus collection.
        
        Args:
            resume: ResumeDocument object with vector embeddings
            
        Returns:
            Document ID of the stored resume
        """
        if not resume.vector:
            raise ValueError("Resume must have vector embeddings before storing")
        
        try:
            collection = Collection(self.collection_name)
            
            # Insert data
            data = [
                [resume.doc_id],
                [resume.filename],
                [str(resume.file_path)],
                [resume.content],
                [resume.metadata],
                [resume.vector]
            ]
            
            collection.insert(data)
            logger.info(f"Stored resume in Milvus: {resume.filename} (ID: {resume.doc_id})")
            return resume.doc_id
            
        except Exception as e:
            logger.error(f"Failed to store resume {resume.filename}: {str(e)}")
            raise