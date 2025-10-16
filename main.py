from fastapi import FastAPI, HTTPException
from models import TaskPayload, PromptPayload
from handlers.generic_handler import handle_task
from utils import llm_ops
import os
from dotenv import load_dotenv

load_dotenv()
EXPECTED_SECRET = os.getenv("TDS_SECRET")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI is live. Use POST /solve to submit tasks."}


@app.post("/solve")
async def solve(payload: TaskPayload):
    if payload.secret != EXPECTED_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret key")
    try:
        response = await handle_task(payload)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
def generate(prompt_payload: PromptPayload):
    """Generate text from the configured LLM.

    This endpoint is a thin wrapper around `utils.llm_ops.query_llm` and
    returns the raw LLM JSON response. It intentionally raises a 500
    HTTP error if the LLM call fails.
    """
    try:
        resp = llm_ops.query_llm(prompt_payload.prompt)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
