import os
import requests

def query_llm(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    url = os.getenv("OPENAI_BASE_URL") + "/chat/completions"
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
