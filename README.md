# 23F2002036-TDS-Project1
Building a Fast API application that receives &amp; verifies a request containing an app brief, using an LLM-assisted generator and deployes to GitHub Pages.

# TDS Project 1 – General Task Solver
This FastAPI application receives a task brief, validates it using a secret key, and dynamically generates a GitHub Pages app using LLM assistance. It’s designed for reproducibility, ethical deployment, and grader-friendly evaluation.

## How It Works
- Accepts POST request with task details
- Validates secret key securely via .env
- Generates a GitHub repo with brief-based content
- Enables GitHub Pages for public access
- Returns metadata including repo URL, commit SHA, and live Pages link

## Setup
- Clone repo
- Add `.env` with secret and GitHub token
- Install Dependencies
- Run with `uvicorn main:app --reload`

## API Endpoint POST /solve
- Payload Example:
{
  "email": "student@example.com",
  "secret": "...",
  "task": "captcha-solver-...",
  "round": 1,
  "nonce": "ab12-...",
  "brief": "Create a captcha solver that handles ?url=https://.../image.png. Default to attached sample.",
  "checks": [
    "Repo has MIT license"
    "README.md is professional",
    "Page displays captcha URL passed at ?url=...",
    "Page displays solved captcha text within 15 seconds",
  ],
  "evaluation_url": "https://example.com/notify",
  "attachments": [{ "name": "sample.png", "url": "data:image/png;base64,iVBORw..." }]
}

## Response Example
- {
  "repo_url": "https://github.com/username/generated-repo",
  "commit_sha": "abc123def456",
  "pages_url": "https://username.github.io/generated-repo/"
}

## Testing
- Run included test scripts:
- python test_fastapi.py
- python test_solve.py

## Repo Hygine
- .gitignore excludes venv, .env, and cache files
- Modular structure: handlers, utils, playwright, tests
- Swagger metadata added for clarity

## License
MIT

