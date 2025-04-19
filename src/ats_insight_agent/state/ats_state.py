from pydantic import BaseModel, Field
from typing import Any, Dict, Literal, Optional
import json
import src.ats_insight_agent.utils.constants as const

    
   
class ATSState(BaseModel):
    """
    Represents the structure of the state used in the SDLC graph

    """    
    pass
    
    
    
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is any kind of Pydantic model
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        # Or check for specific classes if needed
        # if isinstance(obj, UserStories) or isinstance(obj, DesignDocument):
        #     return obj.model_dump()
        return super().default(obj)
    

    