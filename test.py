import requests

payload = {
    
  # Student email ID
  "email": "student@example.com",
  # Student-provided secret
  "secret": "monika-proj-1",
  # A unique task ID.
  "task": "captcha-solver-monika",
  # There will be multiple rounds per task. This is the round index
  "round": 1,
  # Pass this nonce back to the evaluation URL below
  "nonce": "ab12-...",
  # brief: mentions what the app needs to do
  "brief": "Create a captcha solver that handles ?url=https://.../image.png. Default to attached sample.",
  # checks: mention how it will be evaluated
  "checks": [
    "Repo has MIT license"
    "README.md is professional",
    "Page displays captcha URL passed at ?url=...",
    "Page displays solved captcha text within 15 seconds",
  ],
  # Send repo & commit details to the URL below
  "evaluation_url": "https://example.com/notify",
  # Attachments will be encoded as data URIs
  "attachments": [{ "name": "sample.png", "url": "data:image/png;base64,iVBORw..." }]
}

res = requests.post("http://127.0.0.1:8000/solve", json=payload)
print(res.json())