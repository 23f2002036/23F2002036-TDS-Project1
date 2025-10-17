from fastapi import FastAPI, HTTPException
from models import TaskPayload, PromptPayload
from handlers.generic_handler import handle_task
from utils import llm_ops
import os
from dotenv import load_dotenv
import requests

load_dotenv()
EXPECTED_SECRET = os.getenv("TDS_SECRET")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI is live. Use POST /solve to submit tasks."}

from fastapi.responses import JSONResponse
import logging
logger = logging.getLogger("uvicorn")

@app.post(
    "/solve",
    summary="Submit a task brief",
    description="Validates secret and generates a GitHub Pages app using LLM assistance",
    response_description="Returns repo URL, commit SHA, and GitHub Pages URL"
)
async def solve(payload: TaskPayload):
    logger.info(f"Received payload: {payload.dict()}")

    if payload.secret != EXPECTED_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret key")

    try:
        response = await handle_task(payload)
        return JSONResponse(status_code=200, content=response)
    except requests.exceptions.HTTPError as e:
        logger.error(f"LLM error: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"LLM error: {e.response.text}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
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
