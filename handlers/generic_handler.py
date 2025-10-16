from utils.github_ops import create_repo_and_push, create_or_update_repo, poll_pages_url
from utils import llm_ops
import requests
import json
from jsonschema import validate, ValidationError
import base64
import time


def _decode_attachments(attachments):
    files = {}
    if not attachments:
        return files
    for att in attachments:
        name = att.get("name")
        url = att.get("url")
        if not name or not url:
            continue
        # data URI format: data:[<mediatype>][;base64],<data>
        try:
            header, data = url.split(",", 1)
            if header.endswith(";base64"):
                content = base64.b64decode(data)
                # store binary as base64-encoded text file so repo can save it
                files[name] = content.decode("latin1")
            else:
                files[name] = data
        except Exception:
            # fallback: save the url as a text file
            files[name] = url
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


async def handle_task(payload):
    repo_name = f"{payload.task}-{payload.nonce}"

    # Build a prompt for the LLM to return a JSON mapping of files
    # Use .format with doubled braces to include literal JSON braces safely
    prompt_template = (
        "You are a code generator. Produce a JSON object mapping file paths to file contents for a minimal web app "
        "that fulfills this brief: {brief}\n\n"
        "Return strictly a single JSON object (no surrounding text). The object must be a mapping from file path strings to file content strings. "
        "Example: {{\"index.html\": \"<html><body>Hello</body></html>\"}}. Do NOT include any additional commentary."
    )
    prompt = prompt_template.format(brief=payload.brief)

    # include attachments info in the prompt if present
    if getattr(payload, "attachments", None):
        prompt += "\nAttachments: " + json.dumps(payload.attachments)

    def validate_files_mapping(obj):
        """Return (is_valid, errors). Valid if obj is a dict with string keys and string or bytes values."""
        schema = {
            "type": "object",
            "additionalProperties": {"anyOf": [{"type": "string"}, {"type": "array"}]},
        }
        try:
            validate(instance=obj, schema=schema)
            return True, None
        except ValidationError as e:
            return False, str(e)

    # Try querying the LLM with a few retries if parsing fails
    llm_resp = None
    llm_text = None
    max_llm_attempts = 3
    for attempt in range(max_llm_attempts):
        try:
            llm_resp = llm_ops.query_llm(prompt)
        except Exception as e:
            if attempt == max_llm_attempts - 1:
                raise RuntimeError(f"LLM query failed: {e}")
            time.sleep(1 * (attempt + 1))
            continue

        # extract text
        try:
            if isinstance(llm_resp, dict) and "choices" in llm_resp:
                choices = llm_resp.get("choices")
                if choices and isinstance(choices, list):
                    llm_text = choices[0].get("message", {}).get("content") or choices[0].get("text")
            elif isinstance(llm_resp, str):
                llm_text = llm_resp
            else:
                llm_text = str(llm_resp)
        except Exception:
            llm_text = str(llm_resp)

        # attempt to parse JSON; if success break, else retry
        parsed = None
        if llm_text:
            try:
                parsed = json.loads(llm_text)
            except Exception:
                parsed = None

        # If parsed, validate structure
        if parsed:
            ok, err = validate_files_mapping(parsed)
            if ok:
                break
            else:
                parsed = None
                # ask the LLM again with a stricter prompt explaining the error
                if attempt < max_llm_attempts - 1:
                    prompt = (
                        "Your previous response did not match the required JSON schema: "
                        f"{err}.\nReturn only a single JSON object mapping file path strings to file content strings. "
                        "No extra text. Example: {\"index.html\": \"<html>...</html>\"}."
                    )
                    time.sleep(1)
                    continue
        # if not parsed, attempt to clean text blocks (strip fences) and try again
        if llm_text:
            cleaned = llm_text
            # remove triple backticks and language hints
            cleaned = cleaned.replace("```json", "").replace("```", "")
            # find first '{' and last '}'
            try:
                start = cleaned.index("{")
                end = cleaned.rindex("}")
                candidate = cleaned[start:end+1]
                try:
                    parsed = json.loads(candidate)
                except Exception:
                    parsed = None
            except ValueError:
                parsed = None

        if parsed:
            llm_text = candidate
            ok, err = validate_files_mapping(parsed)
            if ok:
                break
            else:
                # continue loop to retry
                parsed = None
        # otherwise retry the LLM
        if attempt < max_llm_attempts - 1:
            time.sleep(1 * (attempt + 1))

    # if we have parsed JSON mapping, use it; else we'll use raw text fallback

    # Try to extract text from common response shapes
    text = None
    try:
        # OpenAI-style chat completion
        if isinstance(llm_resp, dict) and "choices" in llm_resp:
            choices = llm_resp.get("choices")
            if choices and isinstance(choices, list):
                text = choices[0].get("message", {}).get("content") or choices[0].get("text")
    except Exception:
        text = None

    files = {}
    # decode attachments into files mapping
    files.update(_decode_attachments(getattr(payload, "attachments", None)))

    if parsed and isinstance(parsed, dict):
        files.update(parsed)
    else:
        # fallback: use the llm_text or brief inside index.html
        body_text = (llm_text or payload.brief or "Generated app")
        files["index.html"] = f"<html><body><pre>{body_text}</pre></body></html>"

    # Create repo and push files
    # For round 2, attempt to update existing repo instead of creating a fresh one
    try:
        if getattr(payload, "round", 1) >= 2:
            repo_url, commit_sha, pages_url = create_or_update_repo(repo_name, payload.brief, files, update_if_exists=True)
        else:
            repo_url, commit_sha, pages_url = create_or_update_repo(repo_name, payload.brief, files, update_if_exists=False)
    except RuntimeError:
        # race: repo exists when creating new; try update instead
        repo_url, commit_sha, pages_url = create_or_update_repo(repo_name, payload.brief, files, update_if_exists=True)

    response_payload = {
        "email": payload.email,
        "task": payload.task,
        "round": payload.round,
        "nonce": payload.nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    # Poll pages_url to verify it's live (best-effort)
    try:
        poll_pages_url(pages_url, timeout=120, interval=5)
    except Exception:
        pass

    # Notify evaluation endpoint with retries
    _post_with_retries(payload.evaluation_url, response_payload)

    return response_payload
