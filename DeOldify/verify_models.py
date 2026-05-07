import hashlib
import json
import os
import sys


def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():
    if not os.path.exists("models.json"):
        print("Error: models.json not found.")
        sys.exit(1)

    with open("models.json", "r") as f:
        manifest = json.load(f)

    all_passed = True
    print("Verifying models...")

    # Check both root and models/ directory
    search_paths = [".", "models"]

    for filename, expected_hash in manifest.items():
        found = False
        for path in search_paths:
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath):
                found = True
                print(f"Checking {filename}...", end=" ")
                actual_hash = calculate_sha256(filepath)
                if actual_hash == expected_hash:
                    print("PASS")
                else:
                    print(
                        f"FAIL (Expected {expected_hash[:8]}..., got {actual_hash[:8]}...)"
                    )
                    all_passed = False
                break

        if not found:
            # It's okay if a model isn't present, but if it IS present it MUST match.
            # However, for a verification script, maybe we want to warn?
            # Let's just say "Not present (Skipped)"
            print(f"Checking {filename}... Not found (Skipped)")

    if all_passed:
        print("\nAll present models verified successfully.")
        sys.exit(0)
    else:
        print("\nVerification FAILED for some models.")
        sys.exit(1)


if __name__ == "__main__":
    main()
