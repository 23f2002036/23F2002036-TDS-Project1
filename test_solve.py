from fastapi.testclient import TestClient
import main

# Mock llm and github ops

def dummy_query_llm(prompt):
    # Return a JSON mapping as string inside choices to simulate the LLM
    return {"choices": [{"message": {"content": '{"index.html": "<html><body><h1>Hello</h1></body></html>"}'}}]}


def dummy_create_or_update(repo_name, brief, files, update_if_exists=False):
    # Simulate creating repo and returning URLs
    return (f"https://github.com/fake/{repo_name}", "deadbeef", f"https://fake.github.io/{repo_name}/")


client = TestClient(main.app)


def test_solve_happy_path(monkeypatch):
    monkeypatch.setenv("TDS_SECRET", "monika-proj-1")
    # monkeypatch the llm and github ops
    monkeypatch.setattr(main.llm_ops, "query_llm", dummy_query_llm)
    import utils.github_ops as gh
    # handlers imported create_or_update_repo and poll_pages_url into its module namespace; patch both places
    import handlers.generic_handler as h
    monkeypatch.setattr(gh, "create_or_update_repo", dummy_create_or_update)
    monkeypatch.setattr(h, "create_or_update_repo", dummy_create_or_update)
    # avoid polling external pages in tests
    monkeypatch.setattr(gh, "poll_pages_url", lambda url, timeout=120, interval=5: True)
    monkeypatch.setattr(h, "poll_pages_url", lambda url, timeout=120, interval=5: True)

    payload = {
        "email": "student@example.com",
        "secret": "monika-proj-1",
        "task": "test-task",
        "round": 1,
        "nonce": "nonce123",
        "brief": "Create a hello world page",
        "evaluation_url": "https://example.com/notify"
    }

    res = client.post("/solve", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert body["repo_url"].startswith("https://github.com/fake/")
    assert body["pages_url"].startswith("https://fake.github.io/")
