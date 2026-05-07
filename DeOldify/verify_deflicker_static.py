import ast
import sys


def verify_deflicker_static(file_path):
    print(f"Verifying {file_path} using AST...")

    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    class_found = False
    methods_to_check = [
        "colorize_from_url",
        "colorize_from_file_name",
        "_build_video",
        "_colorize_from_path",
    ]

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "VideoColorizer":
            class_found = True
            print("Found VideoColorizer class.")

            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name in methods_to_check:
                    args = [arg.arg for arg in item.args.args]
                    # Check kwonlyargs as well (arguments after *)
                    kwonlyargs = [arg.arg for arg in item.args.kwonlyargs]
                    all_args = args + kwonlyargs

                    if "deflicker" in all_args:
                        print(f"✅ {item.name} accepts 'deflicker'")
                    else:
                        print(f"❌ {item.name} MISSING 'deflicker'")

    if not class_found:
        print("❌ VideoColorizer class NOT found!")


if __name__ == "__main__":
    verify_deflicker_static("deoldify/visualize.py")
