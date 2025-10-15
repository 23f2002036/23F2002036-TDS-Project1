from pydantic import BaseModel

class TaskPayload(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    brief: str
    secret: str
    evaluation_url: str
