from pydantic import BaseModel
from typing import Optional, List

class Observation(BaseModel):
    email_id: int
    subject: str
    body: str
    history: List[str]

class Action(BaseModel):
    action_type: str  # classify / reply / escalate / ignore
    category: Optional[str] = None
    priority: Optional[str] = None
    response: Optional[str] = None

class Reward(BaseModel):
    value: float