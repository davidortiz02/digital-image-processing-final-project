import subprocess
import json
import base64
import re


def check_repo_file(repo, path):
    cmd = ["gh", "api", f"repos/{repo}/contents/{path}", "--jq", ".content"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        content_b64 = result.stdout.strip()
        content = base64.b64decode(content_b64).decode("utf-8")

        urls = re.findall(r'https?://[^\s"\'<>]+(?:\.onnx|\.pth)', content)
        return urls

    except Exception as e:
        return []


repos = ["thookham/DeOldify-on-Browser"]
files = ["original/index.html", "quantized/index.html"]

all_urls = []
for repo in repos:
    for file in files:
        urls = check_repo_file(repo, file)
        all_urls.extend(urls)

with open("found_urls.txt", "w") as f:
    for url in all_urls:
        f.write(url + "\n")
