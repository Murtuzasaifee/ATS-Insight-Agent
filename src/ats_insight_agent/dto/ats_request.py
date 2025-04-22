from pydantic import BaseModel, Field
from typing import Optional

class ATSRequest(BaseModel):
      
   file_path: str = Field(default=None, description="Path to the resume file")
