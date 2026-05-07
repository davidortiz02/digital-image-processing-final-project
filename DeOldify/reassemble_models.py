import os
import glob

# Configuration
SPLIT_FILES = [
    "ColorizeStable_PretrainOnly_gen.pth",
    "ColorizeVideo_PretrainOnly_gen.pth",
]


def reassemble_file(filename):
    # Find all chunks
    chunks = sorted(glob.glob(f"{filename}.*"))
    if not chunks:
        print(f"No chunks found for {filename}")
        return False

    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping reassembly.")
        return True

    print(f"Reassembling {filename} from {len(chunks)} chunks...")
    with open(filename, "wb") as outfile:
        for chunk in chunks:
            print(f"  Reading {chunk}...")
            with open(chunk, "rb") as infile:
                outfile.write(infile.read())

    print(f"  Created {filename}")
    return True


def main():
    for filename in SPLIT_FILES:
        reassemble_file(filename)


if __name__ == "__main__":
    main()
