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

        print(f"--- Checking {repo}/{path} ---")
        # Search for .onnx or .pth links
        urls = re.findall(r'https?://[^\s"\'<>]+(?:\.onnx|\.pth)', content)
        for url in urls:
            print(f"Found URL: {url}")

    except subprocess.CalledProcessError as e:
        print(f"Error fetching {path}: {e}")
    except Exception as e:
        print(f"Error processing {path}: {e}")


repos = ["thookham/DeOldify-on-Browser", "akbartus/DeOldify-on-Browser"]
files = ["original/index.html", "quantized/index.html"]

for repo in repos:
    for file in files:
        check_repo_file(repo, file)
