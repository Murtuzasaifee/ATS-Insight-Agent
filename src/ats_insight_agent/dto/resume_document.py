from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ResumeDocument(BaseModel):
    """Model representing a parsed resume document."""
    doc_id: str
    filename: str
    file_path: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    vector: Optional[List[float]] = None