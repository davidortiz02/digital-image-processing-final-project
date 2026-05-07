"""
Download and Convert DeOldify Models to ONNX for Browser Use

Downloads PyTorch models from original sources and converts them to ONNX format
for use in DeOldify-on-Browser.

Usage:
    python download_and_convert_to_onnx.py

Requirements:
    pip install torch torchvision onnx requests tqdm

The converted ONNX files can then be uploaded to HuggingFace using:
    huggingface-cli upload thookham/DeOldify-on-Browser ./models/*.onnx
"""

import os
import sys
import hashlib
import requests
from pathlib import Path
from tqdm import tqdm

# Configuration
MODELS_DIR = Path(__file__).parent.parent / "models"

# Original model download URLs (from jantic/DeOldify)
GENERATOR_URLS = {
    "ColorizeArtistic_gen.pth": "https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth",
    "ColorizeStable_gen.pth": "https://www.dropbox.com/s/axsd2g85uyixaho/ColorizeStable_gen.pth?dl=1",
    "ColorizeVideo_gen.pth": "https://data.deepai.org/deoldify/ColorizeVideo_gen.pth",
}

# Expected SHA256 hashes
EXPECTED_HASHES = {
    "ColorizeArtistic_gen.pth": "3f750246fa220529323b85a8905f9b49c0e5d427099185334d048fb5b5e22477",
    "ColorizeStable_gen.pth": "ca9cd7f43fb8b222c9a70f7b292e305a000694b0ff9d2ae4a6747b1a2e1ee5af",
    "ColorizeVideo_gen.pth": "e3d98bb6a222354c79f95485c2f078a89dc724e9183662506d9e0f5aafac83ad",
}


def calculate_sha256(filepath):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def download_file(url, filepath):
    """Download a file with progress bar."""
    print(f"Downloading {filepath.name}...")

    # Handle Dropbox URLs
    if "dropbox.com" in url and "dl=0" in url:
        url = url.replace("dl=0", "dl=1")

    response = requests.get(url, stream=True, allow_redirects=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))

    with open(filepath, "wb") as f, tqdm(
        desc=filepath.name,
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=8192):
            size = f.write(data)
            bar.update(size)

    return True


def convert_to_onnx(pth_path, onnx_path, model_type="artistic"):
    """Convert PyTorch model to ONNX format."""
    print(f"Converting {pth_path.name} to ONNX...")

    try:
        import torch
        import torch.onnx

        # Add parent directory to path for deoldify imports
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from deoldify.generators import gen_inference_deep

        # Create model and load weights
        print(f"  Loading model...")
        model = gen_inference_deep(side=256, n_classes=3)

        # Load state dict
        state_dict = torch.load(pth_path, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()

        # Create dummy input
        dummy_input = torch.randn(1, 1, 256, 256)

        # Export to ONNX
        print(f"  Exporting to ONNX...")
        torch.onnx.export(
            model,
            dummy_input,
            onnx_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=["input"],
            output_names=["output"],
            dynamic_axes={
                "input": {0: "batch_size", 2: "height", 3: "width"},
                "output": {0: "batch_size", 2: "height", 3: "width"},
            },
        )

        print(f"  ✅ Saved to {onnx_path}")
        return True

    except Exception as e:
        print(f"  ❌ Conversion failed: {e}")
        return False


def main():
    MODELS_DIR.mkdir(exist_ok=True)
    print(f"Working directory: {MODELS_DIR}")

    # Step 1: Download generator models
    print("\n" + "=" * 60)
    print("STEP 1: Downloading Generator Models")
    print("=" * 60)

    for filename, url in GENERATOR_URLS.items():
        filepath = MODELS_DIR / filename

        if filepath.exists():
            print(f"\n{filename} already exists, checking hash...")
            current_hash = calculate_sha256(filepath)
            if current_hash == EXPECTED_HASHES.get(filename, ""):
                print(f"  ✅ Hash verified, skipping download")
                continue
            else:
                print(f"  ⚠️ Hash mismatch, re-downloading...")

        try:
            download_file(url, filepath)

            # Verify hash
            if filename in EXPECTED_HASHES:
                file_hash = calculate_sha256(filepath)
                if file_hash == EXPECTED_HASHES[filename]:
                    print(f"  ✅ Hash verified")
                else:
                    print(
                        f"  ⚠️ Hash mismatch (expected {EXPECTED_HASHES[filename][:16]}...)"
                    )
        except Exception as e:
            print(f"  ❌ Failed: {e}")

    # Step 2: Convert to ONNX (optional)
    print("\n" + "=" * 60)
    print("STEP 2: Convert to ONNX")
    print("=" * 60)
    print("To convert models to ONNX format for browser use,")
    print("run this script with --convert flag (requires PyTorch)")

    if "--convert" in sys.argv:
        for pth_name in GENERATOR_URLS.keys():
            pth_path = MODELS_DIR / pth_name
            onnx_name = (
                pth_name.replace("Colorize", "deoldify-")
                .replace("_gen.pth", ".onnx")
                .lower()
            )
            onnx_path = MODELS_DIR / onnx_name

            if pth_path.exists() and not onnx_path.exists():
                convert_to_onnx(pth_path, onnx_path)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print(f"\nModels saved to: {MODELS_DIR}")
    print("\nTo upload to HuggingFace:")
    print("  huggingface-cli upload thookham/DeOldify-on-Browser ./models/*.onnx")


if __name__ == "__main__":
    main()
