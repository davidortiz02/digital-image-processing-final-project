"""
Export DeOldify PyTorch Models to ONNX format for browser use.

This script properly loads the DeOldify models using their architecture
and exports them to ONNX format compatible with ONNX Runtime Web.

Usage:
    python export_to_onnx.py [model_name]

    model_name: artistic, stable, video, or all (default: all)

Requirements:
    - PyTorch weights in models/ folder
    - pip install torch torchvision onnx

Output:
    models/deoldify-artistic.onnx
    models/deoldify-stable.onnx
    models/deoldify-video.onnx
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for deoldify imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import torch.onnx
from torch import nn

# Model configurations
MODEL_CONFIGS = {
    "artistic": {
        "pth_name": "ColorizeArtistic_gen",
        "onnx_name": "deoldify-artistic.onnx",
        "model_type": "deep",
        "arch": "resnet34",
        "nf_factor": 1.5,
    },
    "stable": {
        "pth_name": "ColorizeStable_gen",
        "onnx_name": "deoldify-stable.onnx",
        "model_type": "wide",
        "arch": "resnet101",
        "nf_factor": 2,
    },
    "video": {
        "pth_name": "ColorizeVideo_gen",
        "onnx_name": "deoldify-video.onnx",
        "model_type": "wide",
        "arch": "resnet101",
        "nf_factor": 2,
    },
}


def export_model(model_name: str, models_dir: Path, input_size: int = 256):
    """Export a single model to ONNX format."""
    config = MODEL_CONFIGS[model_name]
    pth_path = models_dir / f"{config['pth_name']}.pth"
    onnx_path = models_dir / config["onnx_name"]

    if not pth_path.exists():
        print(f"X Model not found: {pth_path}")
        return False

    print(f"\n{'='*60}")
    print(f"Exporting {model_name} model")
    print(f"{'='*60}")
    print(f"  Input: {pth_path}")
    print(f"  Output: {onnx_path}")

    try:
        # Import deoldify modules
        from deoldify.generators import gen_inference_deep, gen_inference_wide

        # Load the model using DeOldify's proper loader
        print(f"  Loading model...")
        root_folder = models_dir.parent

        if config["model_type"] == "deep":
            import torchvision.models as models

            learn = gen_inference_deep(
                root_folder=root_folder,
                weights_name=config["pth_name"],
                arch=getattr(models, config["arch"]),
                nf_factor=config["nf_factor"],
            )
        else:  # wide
            import torchvision.models as models

            learn = gen_inference_wide(
                root_folder=root_folder,
                weights_name=config["pth_name"],
                arch=getattr(models, config["arch"]),
                nf_factor=config["nf_factor"],
            )

        model = learn.model
        model.eval()

        # Move to CPU for export
        model = model.cpu()

        # Create dummy input (grayscale image: 1 channel)
        # Input shape: [batch, channels, height, width]
        print(f"  Creating test input ({input_size}x{input_size})...")
        dummy_input = torch.randn(1, 3, input_size, input_size)

        # Export to ONNX
        print(f"  Exporting to ONNX...")
        torch.onnx.export(
            model,
            dummy_input,
            str(onnx_path),
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

        # Verify export
        import onnx

        onnx_model = onnx.load(str(onnx_path))
        onnx.checker.check_model(onnx_model)

        file_size_mb = onnx_path.stat().st_size / (1024 * 1024)
        print(f"  SUCCESS Exported successfully! ({file_size_mb:.1f} MB)")
        return True

    except Exception as e:
        print(f"  FAIL Export failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    models_dir = Path(__file__).parent.parent / "models"
    print(f"Models directory: {models_dir}")

    # Determine which models to export
    if len(sys.argv) > 1:
        model_name = sys.argv[1].lower()
        if model_name == "all":
            models_to_export = list(MODEL_CONFIGS.keys())
        elif model_name in MODEL_CONFIGS:
            models_to_export = [model_name]
        else:
            print(f"Unknown model: {model_name}")
            print(f"Available: {', '.join(MODEL_CONFIGS.keys())}, or 'all'")
            sys.exit(1)
    else:
        models_to_export = list(MODEL_CONFIGS.keys())

    print(f"Will export: {', '.join(models_to_export)}")

    # Export each model
    results = {}
    for name in models_to_export:
        results[name] = export_model(name, models_dir)

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    for name, success in results.items():
        status = "SUCCESS" if success else "FAIL"
        print(f"  {status} {name}")

    print(f"\nONNX files saved to: {models_dir}")


if __name__ == "__main__":
    main()
