import os
import requests
from fastapi import HTTPException

def query_llm(prompt, model="openai/gpt-3.5-turbo"):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    url = os.getenv("OPENAI_BASE_URL") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise HTTPException(status_code=500, detail="LLM processing failed")

# Validate LLM response
def extract_files(llm_response):
    if "files" not in llm_response:
        raise HTTPException(status_code=500, detail="Missing 'files' in LLM response")
    return llm_response["files"]
