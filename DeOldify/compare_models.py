import hashlib
import requests
import os


def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def download_file(url, filename):
    print(f"Downloading {url}...")
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename


external_urls = {
    "glitch_art.onnx": "https://huggingface.co/thookham/DeOldify-on-Browser/resolve/main/deoldify-art.onnx",
    "glitch_quant.onnx": "https://huggingface.co/thookham/DeOldify-on-Browser/resolve/main/deoldify-quant.onnx",
}

# Local files
local_files = {
    "local_art.onnx": "models/deoldify-art.onnx",
    "local_quant.onnx": "models/deoldify-quant.onnx",
}

print("--- Local File Hashes ---")
for name, path in local_files.items():
    if os.path.exists(path):
        print(f"{name}: {get_file_hash(path)}")
    else:
        print(f"{name}: File not found")

print("\n--- External File Hashes ---")
for name, url in external_urls.items():
    try:
        download_file(url, name)
        print(f"{name}: {get_file_hash(name)}")
    except Exception as e:
        print(f"Error downloading {name}: {e}")
