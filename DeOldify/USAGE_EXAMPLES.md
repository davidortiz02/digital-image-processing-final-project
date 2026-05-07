# DeOldify Usage Examples

This guide provides practical examples for using DeOldify models from Hugging Face.

## Quick Start

### Install Dependencies

```bash
pip install huggingface_hub torch torchvision Pillow numpy
```

### Download a Model

```python
from huggingface_hub import hf_hub_download

# Download the Stable model (recommended for portraits)
model_path = hf_hub_download(
    repo_id="thookham/DeOldify",
    filename="ColorizeStable_gen.pth"
)

print(f"Model downloaded to: {model_path}")
```

## Using PyTorch Models

> **Note**: The full DeOldify package is required to load and use the PyTorch models. Clone the repository: `git clone https://github.com/thookham/DeOldify`

### Example: Colorize an Image

```python
from deoldify import device
from deoldify.visualize import get_image_colorizer
from PIL import Image

# Initialize colorizer (will download model if needed)
colorizer = get_image_colorizer(artistic=False)  # Use Stable model

# Colorize an image
source_path = "old_photo.jpg"
result_path = colorizer.plot_transformed_image(
    path=source_path,
    render_factor=35,  # Higher = better quality, slower
    compare=True  # Show before/after
)

print(f"Colorized image saved to: {result_path}")
```

### Example: Batch Processing

```python
from pathlib import Path
from deoldify.visualize import get_image_colorizer

colorizer = get_image_colorizer(artistic=True)  # Use Artistic model

input_dir = Path("black_and_white_photos")
output_dir = Path("colorized")
output_dir.mkdir(exist_ok=True)

for img_path in input_dir.glob("*.jpg"):
    print(f"Processing {img_path.name}...")
    result = colorizer.get_transformed_image(
        path=str(img_path),
        render_factor=30
    )
    result.save(output_dir / img_path.name)

print(f"Processed {len(list(input_dir.glob('*.jpg')))} images")
```

## Using ONNX Models (Browser)

The ONNX models can run directly in web browsers using ONNX Runtime Web.

### Example: HTML Page

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js"></script>
</head>
<body>
  <input type="file" id="imageInput" accept="image/*" />
  <canvas id="outputCanvas"></canvas>

  <script>
    async function loadAndColorize() {
      // Load model from Hugging Face
      const session = await ort.InferenceSession.create(
        "https://huggingface.co/thookham/DeOldify/resolve/main/deoldify-quant.onnx"
      );

      document.getElementById('imageInput').addEventListener('change', async (e) => {
        const file = e.target.files[0];
        const image = new Image();
        image.src = URL.createObjectURL(file);
        
        image.onload = async () => {
          // Preprocessing (resize to 256x256, convert to Float32 tensor)
          const canvas = document.createElement('canvas');
          canvas.width = 256;
          canvas.height = 256;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(image, 0, 0, 256, 256);
          
          const imageData = ctx.getImageData(0, 0, 256, 256);
          // ... (preprocessing code)
          
          // Run inference
          const tensor = new ort.Tensor('float32', processedData, [1, 3, 256, 256]);
          const results = await session.run({ input: tensor });
          
          // Display result
          // ... (postprocessing code)
        };
      });
    }

    loadAndColorize();
  </script>
</body>
</html>
```

For a complete working example, see the [browser directory](https://github.com/thookham/DeOldify/tree/master/browser) in the GitHub repository.

## Model Selection Guide

### Artistic Model
- **Best for**: General historical photos, artistic colorization
- **Pros**: Most vibrant colors, interesting details
- **Cons**: May require `render_factor` tuning
- **Files**: `ColorizeArtistic_gen.pth`, `deoldify-art.onnx`

```python
colorizer = get_image_colorizer(artistic=True)
```

### Stable Model
- **Best for**: Portraits, landscapes
- **Pros**: More consistent, less artifacts
- **Cons**: Slightly less colorful than Artistic
- **Files**: `ColorizeStable_gen.pth`

```python
colorizer = get_image_colorizer(artistic=False)
```

### Video Model
- **Best for**: Video colorization
- **Pros**: Flicker-free, temporally consistent
- **Cons**: Least colorful of the three
- **Files**: `ColorizeVideo_gen.pth`

```python
from deoldify.visualize import get_video_colorizer
video_colorizer = get_video_colorizer()
```

## Advanced Usage

### Custom Render Factor

The `render_factor` parameter controls quality vs speed:

```python
# Low quality, fast (good for testing)
result = colorizer.get_transformed_image(path="photo.jpg", render_factor=10)

# High quality, slow (best results)
result = colorizer.get_transformed_image(path="photo.jpg", render_factor=45)

# Recommended range: 20-40
```

### Using Critic Weights (Training)

If you want to continue training the models:

```python
from huggingface_hub import hf_hub_download

# Download both generator and critic
gen_path = hf_hub_download(repo_id="thookham/DeOldify", filename="ColorizeArtistic_gen.pth")
crit_path = hf_hub_download(repo_id="thookham/DeOldify", filename="ColorizeArtistic_crit.pth")

# Load for training (see full documentation in GitHub repo)
```

## Troubleshooting

### "CUDA out of memory"
- Reduce `render_factor`
- Process smaller images
- Close other GPU applications

### "Module 'deoldify' not found"
- Install the DeOldify package: Clone the repo and run `pip install -e .`

### Colors look unrealistic
- Try the Stable model instead of Artistic
- Adjust `render_factor` (try values between 20-40)
- Some images may not colorize well due to damage or low quality

## Additional Resources

- **GitHub Repository**: https://github.com/thookham/DeOldify
- **Setup Guides**:
  - [NVIDIA GPU Setup](nvidia_setup.md)
  - [Intel GPU Setup](intel_gpu_setup.md)
- **Model Weights**: All available in this HF repository
- **Browser Demo**: See `browser/` folder in GitHub repo

## Citation

```bibtex
@misc{deoldify,
  author = {Antic, Jason},
  title = {DeOldify},
  year = {2019},
  publisher = {GitHub},
  url = {https://github.com/jantic/DeOldify}
}
```
