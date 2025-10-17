import json
import base64
import time
import requests
from jsonschema import validate, ValidationError
from utils.github_ops import create_or_update_repo, poll_pages_url
from utils import llm_ops


def _decode_attachments(attachments):
    files = {}
    if not attachments:
        return files
    for att in attachments:
        name = att.get("name")
        url = att.get("url")
        if not name or not url:
            continue
        try:
            header, data = url.split(",", 1)
            if header.endswith(";base64"):
                content = base64.b64decode(data)
                files[name] = content.decode("latin1")
            else:
                files[name] = data
        except Exception:
            files[name] = f"Failed to decode: {url}"
    return files


def _post_with_retries(url, payload, max_retries=5):
    headers = {"Content-Type": "application/json"}
    delay = 1
    for attempt in range(max_retries):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(delay)
        delay *= 2
    return False


def _validate_files_mapping(obj):
    schema = {
        "type": "object",
        "additionalProperties": {"anyOf": [{"type": "string"}, {"type": "array"}]},
    }
    try:
        validate(instance=obj, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)


def _extract_llm_text(llm_resp):
    if isinstance(llm_resp, dict) and "choices" in llm_resp:
        choices = llm_resp.get("choices")
        if choices and isinstance(choices, list):
            return choices[0].get("message", {}).get("content") or choices[0].get("text")
    elif isinstance(llm_resp, str):
        return llm_resp
    return str(llm_resp)


async def handle_task(payload):
    repo_name = f"{payload.task}-{payload.nonce}"

    prompt = (
        "You are a code generator. Produce a JSON object mapping file paths to file contents for a minimal web app "
        f"that fulfills this brief: {payload.brief}\n\n"
        "Return strictly a single JSON object (no surrounding text). "
        "Example: {\"index.html\": \"<html><body>Hello</body></html>\"}."
    )

    if payload.attachments:
        prompt += "\nAttachments: " + json.dumps(payload.attachments)

    parsed = None
    llm_text = None
    for attempt in range(3):
        try:
            llm_resp = llm_ops.query_llm(prompt, payload.model)
            llm_text = _extract_llm_text(llm_resp)
            parsed = json.loads(llm_text)
            ok, err = _validate_files_mapping(parsed)
            if ok:
                break
            else:
                parsed = None
                prompt = (
                    f"Your previous response did not match the required JSON schema: {err}.\n"
                    "Return only a single JSON object mapping file path strings to file content strings. "
                    "No extra text. Example: {\"index.html\": \"<html>...</html>\"}."
                )
        except Exception:
            time.sleep(1 * (attempt + 1))

        if not parsed and llm_text:
            cleaned = llm_text.replace("```json", "").replace("```", "")
            try:
                candidate = cleaned[cleaned.index("{"):cleaned.rindex("}") + 1]
                parsed = json.loads(candidate)
                ok, err = _validate_files_mapping(parsed)
                if not ok:
                    parsed = None
            except Exception:
                parsed = None

    files = _decode_attachments(payload.attachments)
    if parsed:
        files.update(parsed)
    else:
        fallback = llm_text or payload.brief or "Generated app"
        files["index.html"] = f"<html><body><pre>{fallback}</pre></body></html>"

    try:
        repo_url, commit_sha, pages_url = create_or_update_repo(
            repo_name, payload.brief, files,
            update_if_exists=(payload.round or 1) >= 2
        )
    except RuntimeError:
        repo_url, commit_sha, pages_url = create_or_update_repo(
            repo_name, payload.brief, files, update_if_exists=True
        )

    response_payload = {
        "email": payload.email,
        "task": payload.task,
        "round": payload.round,
        "nonce": payload.nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    try:
        poll_pages_url(pages_url, timeout=120, interval=5)
    except Exception:
        pass

    _post_with_retries(payload.evaluation_url, response_payload)
    return response_payload