from pydantic import BaseModel, Field
from typing import List

class Config(BaseModel):
    """Configuration for the resume processor."""
    collection_name: str = Field(default="resumes")
    collection_desc: str = Field(default="Resume collection")
    index_file_size: int = Field(default=32)
    vector_dim: int = Field(default=768)
    supported_extensions: List[str] = Field(default=[".pdf", ".docx", ".html"])