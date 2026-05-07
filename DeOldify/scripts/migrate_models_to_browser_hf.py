import os
import sys
import json
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download, upload_file

# Configuration
SOURCE_REPO = "thookham/DeOldify"
TARGET_REPO = "thookham/DeOldify-on-Browser"
TEMP_DIR = Path(__file__).parent.parent / "models" / "_migration_temp"
MODELS_JSON = Path(__file__).parent.parent / "models.json"

# ONNX models (browser-ready)
ONNX_MODELS = {
    "deoldify-art.onnx": "be026e17c47c85527b3084cacad352f7ca0e021c33aa827062c5997ebe72c61f",
    "deoldify-quant.onnx": "35c3fb7ec52122e30e98ed03fa5082b175d0beb7951d62f8bc2178870229e44a",
}


def load_model_list(onnx_only=True):
    """Load model list from models.json"""
    with open(MODELS_JSON, "r") as f:
        all_models = json.load(f)

    if onnx_only:
        return {k: v for k, v in all_models.items() if k.endswith(".onnx")}
    return all_models


def migrate_models(onnx_only=True):
    """Migrate models from source to target repo."""
    api = HfApi()

    # Load models
    models = load_model_list(onnx_only=onnx_only)
    model_type = "ONNX (browser-ready)" if onnx_only else "ALL"
    print(f"Found {len(models)} {model_type} models to migrate")

    # Create temp directory
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    for model_name, expected_hash in models.items():
        print(f"\n{'='*60}")
        print(f"Migrating: {model_name}")
        print(f"{'='*60}")

        local_path = TEMP_DIR / model_name

        # Step 1: Download from source repo
        try:
            print(f"  📥 Downloading from {SOURCE_REPO}...")
            downloaded_path = hf_hub_download(
                repo_id=SOURCE_REPO,
                filename=model_name,
                local_dir=TEMP_DIR,
                local_dir_use_symlinks=False,
            )
            print(f"  ✅ Downloaded to {downloaded_path}")
        except Exception as e:
            print(f"  ❌ Failed to download: {e}")
            continue

        # Step 2: Upload to target repo
        try:
            print(f"  📤 Uploading to {TARGET_REPO}...")
            api.upload_file(
                path_or_fileobj=downloaded_path,
                path_in_repo=model_name,
                repo_id=TARGET_REPO,
                repo_type="model",
                commit_message=f"Add {model_name} from DeOldify",
            )
            print(f"  ✅ Uploaded successfully!")
        except Exception as e:
            print(f"  ❌ Failed to upload: {e}")
            continue

        # Step 3: Clean up temp file
        try:
            os.remove(downloaded_path)
            print(f"  🧹 Cleaned up temp file")
        except:
            pass

    print(f"\n{'='*60}")
    print("Migration complete!")
    print(f"{'='*60}")
    print(f"Check: https://huggingface.co/{TARGET_REPO}/tree/main")


if __name__ == "__main__":
    migrate_models()
