from pydantic import BaseModel
from typing import Optional, List, Any


class TaskPayload(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    brief: str
    secret: str
    evaluation_url: str
    # optional fields present in requests
    attachments: Optional[List[Any]] = None
    checks: Optional[List[str]] = None


class PromptPayload(BaseModel):
    prompt: str
    # optional model identifier for the underlying LLM API
    model: Optional[str] = "openai/gpt-3.5-turbo"
