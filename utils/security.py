import re
from typing import Dict, List


SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_\-]+"),
    re.compile(r"GITHUB_TOKEN", re.I),
    re.compile(r"sk-[A-Za-z0-9_\-\.]+"),
    re.compile(r"-----BEGIN PRIVATE KEY-----"),
]


def scan_for_secrets(files: Dict[str, bytes]) -> List[str]:
    """Return a list of issues found. Files values may be bytes or str."""
    issues = []
    for path, content in files.items():
        if isinstance(content, (bytes, bytearray)):
            try:
                text = content.decode("utf-8", errors="ignore")
            except Exception:
                text = ""
        else:
            text = str(content)
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                issues.append(f"Potential secret in {path}: {pat.pattern}")
    return issues
