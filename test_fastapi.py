from fastapi.testclient import TestClient
import main

# Monkeypatch the llm call to avoid external network requests
class DummyResp:
    def __init__(self, text):
        self.text = text


def dummy_query_llm(prompt):
    return {"choices": [{"message": {"content": f"Echo: {prompt}"}}]}


client = TestClient(main.app)


def test_generate_endpoint():
    # replace the real function with our dummy
    main.llm_ops.query_llm = dummy_query_llm

    payload = {"prompt": "Hello LLM"}
    res = client.post("/generate", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert "choices" in body
    assert body["choices"][0]["message"]["content"] == "Echo: Hello LLM"
