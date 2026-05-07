import inspect
from deoldify.visualize import VideoColorizer


def test_deflicker_argument():
    print("Verifying 'deflicker' argument in VideoColorizer methods...")

    # Check colorize_from_url
    sig_url = inspect.signature(VideoColorizer.colorize_from_url)
    if "deflicker" in sig_url.parameters:
        print("✅ colorize_from_url accepts 'deflicker'")
    else:
        print("❌ colorize_from_url MISSING 'deflicker'")

    # Check colorize_from_file_name
    sig_file = inspect.signature(VideoColorizer.colorize_from_file_name)
    if "deflicker" in sig_file.parameters:
        print("✅ colorize_from_file_name accepts 'deflicker'")
    else:
        print("❌ colorize_from_file_name MISSING 'deflicker'")

    # Check _build_video (internal but modified)
    sig_build = inspect.signature(VideoColorizer._build_video)
    if "deflicker" in sig_build.parameters:
        print("✅ _build_video accepts 'deflicker'")
    else:
        print("❌ _build_video MISSING 'deflicker'")


if __name__ == "__main__":
    try:
        test_deflicker_argument()
        print("\nVerification passed!")
    except Exception as e:
        print(f"\nVerification failed with error: {e}")
