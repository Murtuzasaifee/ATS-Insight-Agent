from pydantic import BaseModel
from typing import Optional
from src.ats_insight_agent.state.ats_state import ATSState
from typing import Dict, Any

class ATSResponse(BaseModel):
    status: str
    message: str
    task_id: Optional[str] = None
    state: Optional[Dict[str, Any]] = None
    error: Optional[str] = None