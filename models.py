from pydantic import BaseModel
from typing import List, Optional


class Email(BaseModel):
    id: str
    subject: str
    body: str
    category: str  # urgent / spam / normal


class Observation(BaseModel):
    emails: List[Email]
    step: int
    reward: float = 0.0
    done: bool = False


class Action(BaseModel):
    email_id: str
    action_type: str  # reply / ignore / escalate
    response: Optional[str] = None