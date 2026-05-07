import os
import sys
import hashlib
import requests
from tqdm import tqdm
from pathlib import Path

# Configuration
MODELS_DIR = Path(__file__).parent.parent / "models"
BASE_URL_HF = "https://huggingface.co/thookham/DeOldify/resolve/main/"

# Model definitions with SHA256 hashes (from models.json)
MODELS = {
    "ColorizeArtistic_gen.pth": "3f750246fa220529323b85a8905f9b49c0e5d427099185334d048fb5b5e22477",
    "ColorizeStable_gen.pth": "ca9cd7f43fb8b222c9a70f7b292e305a000694b0ff9d2ae4a6747b1a2e1ee5af",
    "ColorizeVideo_gen.pth": "e3d98bb6a222354c79f95485c2f078a89dc724e9183662506d9e0f5aafac83ad",
    "deoldify-art.onnx": "be026e17c47c85527b3084cacad352f7ca0e021c33aa827062c5997ebe72c61f",
    "deoldify-quant.onnx": "35c3fb7ec52122e30e98ed03fa5082b175d0beb7951d62f8bc2178870229e44a",
}


def calculate_sha256(filepath):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def download_file(url, filepath, expected_hash=None):
    """Download a file with progress bar and hash verification."""
    print(f"Downloading {filepath.name}...")

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))

    with open(filepath, "wb") as f, tqdm(
        desc=filepath.name,
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

    if expected_hash:
        print("Verifying hash...")
        file_hash = calculate_sha256(filepath)
        if file_hash != expected_hash:
            print(f"❌ Hash mismatch for {filepath.name}!")
            print(f"Expected: {expected_hash}")
            print(f"Got:      {file_hash}")
            return False
        print("✅ Hash verified.")
    return True


def main():
    MODELS_DIR.mkdir(exist_ok=True)
    print(f"Checking models in {MODELS_DIR}...")

    for filename, expected_hash in MODELS.items():
        filepath = MODELS_DIR / filename

        if filepath.exists():
            print(f"\nChecking existing file: {filename}")
            current_hash = calculate_sha256(filepath)
            if current_hash == expected_hash:
                print(f"✅ {filename} is up to date.")
                continue
            else:
                print(f"⚠️ {filename} exists but hash mismatch. Re-downloading...")
        else:
            print(f"\nMissing file: {filename}")

        url = BASE_URL_HF + filename
        try:
            success = download_file(url, filepath, expected_hash)
            if not success:
                print(f"❌ Failed to verify {filename}")
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")

    print("\nDone!")


if __name__ == "__main__":
    main()
