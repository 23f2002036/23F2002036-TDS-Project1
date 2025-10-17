from pydantic import BaseModel, Field
from typing import Optional, List, Any


class TaskPayload(BaseModel):
    email: Optional[str]
    task: Optional[str]
    round: Optional[int]
    nonce: Optional[str]
    brief: Optional[str]
    secret: Optional[str]
    evaluation_url: Optional[str]
    attachments: Optional[List[Any]] = Field(default=[], description="List of file attachments")
    checks: Optional[List[str]] = Field(default=[], description="Validation checks to perform")



class PromptPayload(BaseModel):
    prompt: str
    # optional model identifier for the underlying LLM API
    model: Optional[str] = Field(default="openai/gpt-3.5-turbo", description="LLM model identifier")
