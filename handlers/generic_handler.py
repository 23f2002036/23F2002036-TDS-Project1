from utils.github_ops import create_repo_and_push
import requests

async def handle_task(payload):
    repo_name = f"{payload.task}-{payload.nonce}"
    repo_url, commit_sha, pages_url = create_repo_and_push(repo_name, payload.brief)

    response_payload = {
        "email": payload.email,
        "task": payload.task,
        "round": payload.round,
        "nonce": payload.nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url
    }

    headers = {"Content-Type": "application/json"}
    requests.post(payload.evaluation_url, json=response_payload, headers=headers)

    return response_payload
