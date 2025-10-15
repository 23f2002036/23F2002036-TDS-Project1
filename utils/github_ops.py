from github import Github
import os
import tempfile
import subprocess

def create_repo_and_push(repo_name, brief):
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    g = Github(token)
    user = g.get_user()

    repo = user.create_repo(repo_name, private=False, license_template="mit")
    repo.create_file("README.md", "Initial commit", f"# {repo_name}\n\n{brief}")

    # Generate dummy app code
    app_code = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{repo_name}</title></head>
    <body><h1>{brief}</h1></body>
    </html>
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        subprocess.run(["git", "init"])
        with open("index.html", "w") as f:
            f.write(app_code)
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Add generated app"])
        subprocess.run(["git", "remote", "add", "origin", repo.clone_url])
        subprocess.run(["git", "push", "-u", "origin", "master"])

    repo.enable_pages("master", "/")
    pages_url = f"https://{username}.github.io/{repo_name}/"
    commit_sha = repo.get_commits()[0].sha

    return repo.html_url, commit_sha, pages_url
