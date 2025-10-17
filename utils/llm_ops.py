import os
import requests

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
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

try:
    async def query_llm(prompt, model="openai/gpt-3.5-turbo"):
        response = await call_llm(prompt, model)
        return response

except Exception as e:
    logger.error(f"LLM call failed: {e}")
    raise HTTPException(status_code=500, detail="LLM processing failed")

if "files" not in llm_response:
    raise HTTPException(status_code=500, detail="Missing 'files' in LLM response")
    return llm_response["files"]
