---
license: mit
tags:
- image-colorization
- gan
- computer-vision
- pytorch
- onnx
library_name: pytorch
---

# DeOldify Model Weights

This repository contains pretrained weights for **DeOldify**, a deep learning model for colorizing and restoring old black and white images and videos.

**Original Repository**: [thookham/DeOldify](https://github.com/thookham/DeOldify)  
**Original Author**: Jason Antic ([jantic/DeOldify](https://github.com/jantic/DeOldify))

> [!NOTE]
> This is a **sanitized and modernized fork** maintained by Antigravity. It has been updated for Python 3.11+ compatibility, includes CI/CD pipelines, and has been audited for security.

[![DeOldify CI](https://github.com/thookham/DeOldify/actions/workflows/ci.yml/badge.svg)](https://github.com/thookham/DeOldify/actions/workflows/ci.yml)

## Model Overview

DeOldify uses a Self-Attention Generative Adversarial Network (SAGAN) with a novel **NoGAN** training approach to achieve stable, high-quality colorization without the typical GAN artifacts.

### Three Specialized Models

1. **Artistic** - Highest quality with vibrant colors and interesting details  
   - Best for: General images, historical photos  
   - Backbone: ResNet34 U-Net  
   - Training: 5 NoGAN cycles, 32% ImageNet

2. **Stable** - Best for portraits and landscapes, reduced artifacts  
   - Best for: Faces, nature scenes  
   - Backbone: ResNet101 U-Net  
   - Training: 3 NoGAN cycles, 7% ImageNet

3. **Video** - Optimized for smooth, flicker-free video  
   - Best for: Video colorization, consistency  
   - Backbone: ResNet101 U-Net  
   - Training: Initial cycle only, 2.2% ImageNet

## Available Files

### ONNX Models (Browser/Inference)

| File | Size | Description |
|------|------|-------------|
| `deoldify-art.onnx` | 243 MB | Artistic model in ONNX format for browser use |
| `deoldify-quant.onnx` | 61 MB | Quantized artistic model (75% smaller, slightly lower quality) |

### PyTorch Weights (Training & Inference)

**Generator Weights** (Main):

- `ColorizeArtistic_gen.pth` (243 MB)
- `ColorizeStable_gen.pth` (834 MB)
- `ColorizeVideo_gen.pth` (834 MB)

**Critic Weights** (Main):

- `ColorizeArtistic_crit.pth` (361 MB)
- `ColorizeStable_crit.pth` (361 MB)
- `ColorizeVideo_crit.pth` (361 MB)

**PretrainOnly Weights** (For continued training):

- `ColorizeArtistic_PretrainOnly_gen.pth` (729 MB)
- `ColorizeArtistic_PretrainOnly_crit.pth` (1.05 GB)
- `ColorizeStable_PretrainOnly_crit.pth` (1.05 GB)
- `ColorizeVideo_PretrainOnly_crit.pth` (1.05 GB)

> **Note**: Stable and Video PretrainOnly generators are split files hosted on [GitHub Releases](https://github.com/thookham/DeOldify/releases/tag/v2.0-models).

## Usage

### Browser (ONNX)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js"></script>
</head>
<body>
  <script>
    async function colorize() {
      // Load model from Hugging Face
      const session = await ort.InferenceSession.create(
        "https://huggingface.co/thookham/DeOldify/resolve/main/deoldify-art.onnx"
      );
      
      // Run inference (see full example in GitHub repo)
      // ...
    }
  </script>
</body>
</html>
```

### PyTorch (Python)

```python
from huggingface_hub import hf_hub_download
import torch

# Download model weights
model_path = hf_hub_download(
    repo_id="thookham/DeOldify",
    filename="ColorizeArtistic_gen.pth"
)

# Load weights (requires deoldify package installed)
# See GitHub repository for full usage examples
```

### Installation

```bash
# Clone the main repository
git clone https://github.com/thookham/DeOldify
cd DeOldify

# Install dependencies
pip install -r requirements.txt

# Download a model
from huggingface_hub import hf_hub_download
model = hf_hub_download(repo_id="thookham/DeOldify", filename="ColorizeStable_gen.pth")
```

## Technical Details

### Architecture

- **Generator**: U-Net with ResNet34/101 backbone, spectral normalization, self-attention layers
- **Critic**: PatchGAN discriminator
- **Loss**: Perceptual loss (VGG16) + GAN loss

### NoGAN Training

A novel training approach that combines:

1. Generator pretraining with feature loss
2. Critic pretraining on generated images
3. Short GAN training (30-60 minutes) at inflection point
4. Optional cycle repeats for more colorful results

This eliminates typical GAN artifacts while maintaining realistic colorization.

### Training Data

- Dataset: ImageNet subsets (1-32% depending on model)
- Resolution: 192px during training
- Augmentation: Gaussian noise for video stability

## Model Card

### Model Details

- **Developed by**: Jason Antic (original), Travis Hookham (modernization)
- **Model type**: Conditional GAN for image-to-image translation
- **Language(s)**: N/A (computer vision)
- **License**: MIT
- **Parent Model**: Based on FastAI U-Net and Self-Attention GAN papers

### Intended Use

**Primary Use**: Colorizing black and white photographs and videos  
**Out-of-Scope**: Real-time processing, guaranteed historical accuracy

### Limitations

- Colors may not be historically accurate  
- Performance degrades on very low quality/damaged images
- Artistic model may require render_factor tuning
- Video model trades some color vibrancy for consistency

## Related Models & Resources

### Similar Colorization Models on Hugging Face

**GAN-based Colorization:**

- [Hammad712/GAN-Colorization-Model](https://huggingface.co/Hammad712/GAN-Colorization-Model) - GAN model for grayscale to color transformation
- [jessicanono/filparty_colorization](https://huggingface.co/jessicanono/filparty_colorization) - ResNet-based model for historical photos

**Stable Diffusion-based:**

- [rsortino/ColorizeNet](https://huggingface.co/rsortino/ColorizeNet) - ControlNet adaptation of SD 2.1 for colorization
- [AlekseyCalvin/ColorizeTruer_KontextFluxVar6_BySAP](https://huggingface.co/AlekseyCalvin/ColorizeTruer_KontextFluxVar6_BySAP) - Advanced Flux-based colorization

**Interactive Demos (Spaces):**

- [aryadytm/Photo-Colorization](https://huggingface.co/spaces/aryadytm/Photo-Colorization)
- [Shashank009/Black-And-White-Image-Colorization](https://huggingface.co/spaces/Shashank009/Black-And-White-Image-Colorization)
- [CA611/Image-Colorization](https://huggingface.co/spaces/CA611/Image-Colorization)

### Why Choose DeOldify?

DeOldify stands out for:

- **NoGAN Training**: Unique approach eliminating typical GAN artifacts
- **Specialized Models**: Three purpose-built models (Artistic, Stable, Video)
- **Video Support**: Flicker-free temporal consistency
- **Proven Track Record**: Powers MyHeritage InColor and widely adopted
- **ONNX Support**: Browser-ready models for offline use

## Citation

If you use these models, please cite:

```bibtex
@misc{deoldify,
  author = {Antic, Jason},
  title = {DeOldify},
  year = {2019},
  publisher = {GitHub},
  url = {https://github.com/jantic/DeOldify}
}
```

## Links

- **GitHub Repository**: <https://github.com/thookham/DeOldify>
- **Original DeOldify**: <https://github.com/jantic/DeOldify>
- **MyHeritage InColor** (Commercial version): <https://www.myheritage.com/incolor>
- **Demo (Browser)**: See browser/ folder in GitHub repo

## Model Hosting

Models are hosted on Hugging Face and synced automatically on every push:

| Repository | Models | Use Case |
|------------|--------|----------|
| [thookham/DeOldify](https://huggingface.co/thookham/DeOldify) | PyTorch + ONNX | Training & Inference |
| [thookham/DeOldify-on-Browser](https://huggingface.co/thookham/DeOldify-on-Browser) | ONNX only | Browser deployment |

See [HUGGINGFACE_SYNC.md](docs/HUGGINGFACE_SYNC.md) for sync documentation.

## License

MIT License. See [LICENSE](https://github.com/thookham/DeOldify/blob/master/LICENSE) file.
