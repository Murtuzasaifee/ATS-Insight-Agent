from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ResumeDocument(BaseModel):
    """Model representing a parsed resume document."""
    doc_id: str
    filename: str
    file_path: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    vectors: Optional[List[float]] = None
    chunks: Optional[List[Dict[str, Any]]] = None