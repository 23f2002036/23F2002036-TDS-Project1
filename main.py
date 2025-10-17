from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import TaskPayload, PromptPayload
from handlers.generic_handler import handle_task
from utils import llm_ops
import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EXPECTED_SECRET = os.getenv("TDS_SECRET")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (can restrict origins later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI is live. Use POST /solve to submit tasks."}

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
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def generate(prompt_payload: PromptPayload):
    """
    Generate text from the configured LLM.
    This endpoint wraps `utils.llm_ops.query_llm` and returns the raw LLM JSON response.
    """
    try:
        resp = llm_ops.query_llm(prompt_payload.prompt)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))