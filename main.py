from fastapi import FastAPI, HTTPException
from models import TaskPayload
from handlers.generic_handler import handle_task
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
