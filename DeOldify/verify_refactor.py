import sys
import os
from pathlib import Path
import torch
from unittest.mock import MagicMock, patch

# Add current directory to path
sys.path.append(os.getcwd())

print("Testing imports...")
try:
    import deoldify
    from deoldify import device
    from deoldify.visualize import get_image_colorizer

    print("✅ Imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

print("\nTesting Model Creation (Mocked Weights)...")

# Mock torch.load to avoid needing actual weight files
with patch("torch.load") as mock_load:
    mock_load.return_value = {}  # Empty state dict

    # Mock load_state_dict to accept empty dict
    with patch("torch.nn.Module.load_state_dict") as mock_load_state_dict:
        try:
            # Try to create the colorizer
            # This will build the model architecture using fastai_compat
            colorizer = get_image_colorizer(render_factor=35)
            print("✅ Model instantiated successfully")

            # Verify it's using our compat layer
            print(f"Model type: {type(colorizer.filter.learn.model)}")

        except Exception as e:
            print(f"❌ Model creation failed: {e}")
            import traceback

            traceback.print_exc()
            sys.exit(1)

print("\nTesting Device Detection...")
try:
    import torch

    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device Name: {torch.cuda.get_device_name(0)}")
    print("✅ Device detection passed")
except Exception as e:
    print(f"❌ Device detection failed: {e}")

print("\nRefactor Verification Complete!")
