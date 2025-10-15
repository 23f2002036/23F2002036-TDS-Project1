# 23F2002036-TDS-Project1
Building a Fast API application that receives &amp; verifies a request containing an app brief, using an LLM-assisted generator and deployes to GitHub Pages.

# TDS Project 1 – General Task Solver

This FastAPI app accepts any task brief and dynamically generates a GitHub Pages app based on it.

## How It Works
- Accepts POST request with task details
- Validates secret
- Generates repo with brief-based content
- Enables GitHub Pages
- Responds with metadata

## Setup
- Clone repo
- Add `.env` with secret and GitHub token
- Run with `uvicorn main:app --reload`

## License
MIT

