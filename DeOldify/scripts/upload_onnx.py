from huggingface_hub import HfApi
from pathlib import Path


def main():
    api = HfApi()
    repo_id = "thookham/DeOldify-on-Browser"
    models_dir = Path("models")

    # helper to find files
    files = list(models_dir.glob("deoldify-*.onnx*"))
    print(f"Found {len(files)} files to upload.")

    for file_path in files:
        print(f"Uploading {file_path.name}...")
        try:
            api.upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=file_path.name,
                repo_id=repo_id,
                repo_type="model",
            )
            print("  SUCCESS")
        except Exception as e:
            print(f"  FAIL: {e}")


if __name__ == "__main__":
    main()
