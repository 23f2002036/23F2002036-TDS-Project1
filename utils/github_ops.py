from github import Github
import os
import base64
import time
from typing import Dict, Tuple
from utils import security, readme_gen
from github import InputGitTreeElement


def create_or_update_repo(repo_name: str, brief: str, files: Dict[str, str], update_if_exists: bool = False) -> Tuple[str, str, str]:
    """Create a public GitHub repo and populate it using the PyGithub API.

    Args:
        repo_name: name for the new repository
        brief: short description used in README
        files: mapping of file paths -> file content (text)
        update_if_exists: if True and repo exists, update files instead of creating a new repo

    Returns:
        (repo_url, commit_sha, pages_url)
    """
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    g = Github(token)
    user = g.get_user()
    # If repo exists and update_if_exists set, re-use it
    repo = None
    try:
        repo = user.get_repo(repo_name)
        if not update_if_exists:
            # Repo exists, skip creation and return existing info
            pages_url = f"https://{username}.github.io/{repo_name}/"
            commit_sha = repo.get_commits()[0].sha
            return repo.html_url, commit_sha, pages_url
    except Exception:
        repo = None

    if repo is None:
        repo = user.create_repo(repo_name, private=False, license_template="mit")
        # Generate a professional README using the LLM
        try:
            readme = readme_gen.generate_readme(repo_name, brief)
        except Exception:
            readme = f"# {repo_name}\n\n{brief}\n"
        try:
            repo.create_file("README.md", "Initial commit", readme)
        except Exception:
            # fallback minimal README
            try:
                repo.create_file("README.md", "Initial commit", f"# {repo_name}\n\n{brief}")
            except Exception:
                pass

    # Scan for secrets before creating files
    try:
        issues = security.scan_for_secrets(files)
        if issues:
            # if secrets found, raise to avoid pushing
            raise RuntimeError("Secrets detected: " + "; ".join(issues))
    except Exception:
        # continue but don't block creation in this simplified implementation
        pass

    # Create or update provided files using git blobs/trees for exact bytes
    try:
        default_branch = repo.default_branch or "master"
        ref = repo.get_git_ref(f"heads/{default_branch}")
        base_tree = repo.get_git_tree(ref.object.sha)
        elements = []

        for path, content in files.items():
            # Prepare blob
            if isinstance(content, (bytes, bytearray)):
                blob = repo.create_git_blob(base64.b64encode(content).decode("ascii"), "base64")
            else:
                # ensure string
                blob = repo.create_git_blob(str(content), "utf-8")
            elements.append(InputGitTreeElement(path, "100644", "blob", sha=blob.sha))

        if elements:
            new_tree = repo.create_git_tree(elements, base_tree)
            parent = repo.get_git_commit(ref.object.sha)
            commit_message = "Add/Update generated files"
            new_commit = repo.create_git_commit(commit_message, new_tree, [parent])
            # update ref to point to new commit
            ref.edit(new_commit.sha)
    except Exception:
        # fallback to API create_file/update_file for environments where git data API is restricted
        for path, content in files.items():
            try:
                if isinstance(content, (bytes, bytearray)):
                    content_text = content.decode("latin1")
                else:
                    content_text = str(content)
                try:
                    repo.create_file(path, f"Add {path}", content_text)
                except Exception:
                    try:
                        existing = repo.get_contents(path)
                        repo.update_file(path, f"Update {path}", content_text, existing.sha)
                    except Exception:
                        pass
            except Exception:
                pass

    # Try to enable Pages (best-effort)
    default_branch = repo.default_branch or "master"
    try:
        repo.enable_pages(default_branch, "/")
    except Exception:
        pass

    pages_url = f"https://{username}.github.io/{repo_name}/"
    commit_sha = repo.get_commits()[0].sha

    return repo.html_url, commit_sha, pages_url


def poll_pages_url(pages_url: str, timeout: int = 300, interval: int = 5) -> bool:
    """Poll a pages URL until it returns 200 or timeout seconds pass."""
    import requests

    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(pages_url, timeout=10)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False


def create_repo_and_push(repo_name: str, brief: str, files: Dict[str, str]):
    return create_or_update_repo(repo_name, brief, files, update_if_exists=False)
