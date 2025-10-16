from utils import llm_ops


def generate_readme(repo_name: str, brief: str, pages_url: str = None) -> str:
    prompt = (
        f"Write a professional README.md for a repository named {repo_name}.\n"
        f"Brief: {brief}\n"
        "Include: project summary, setup, usage, evaluation instructions, and license header. "
        "Return only the markdown content."
    )
    resp = llm_ops.query_llm(prompt)
    # extract text
    if isinstance(resp, dict) and "choices" in resp:
        choices = resp.get("choices")
        if choices:
            text = choices[0].get("message", {}).get("content") or choices[0].get("text")
            return text
    return f"# {repo_name}\n\n{brief}\n"
