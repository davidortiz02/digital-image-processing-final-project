---
license: mit
library_name: pytorch
tags:
  - image-colorization
  - image-to-image
  - deoldify
  - gan
  - sagan
  - nogan
  - computer-vision
  - pytorch
  - onnx
  - image-restoration
  - video-colorization
  - resnet
datasets:
  - imagenet-1k
pipeline_tag: image-to-image
language:
  - en
---

<div align="center">

# 🎨 DeOldify

**State-of-the-Art Image & Video Colorization • Modern PyTorch • No FastAI Required**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-ee4c2c.svg)](https://pytorch.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab.svg)](https://python.org/)
[![ONNX](https://img.shields.io/badge/ONNX-Available-orange.svg)](https://onnx.ai/)
[![Browser Demo](https://img.shields.io/badge/🌐_Browser_Demo-Live-brightgreen.svg)](https://deoldify.glitch.me/)

*The legendary AI colorization tool—modernized for PyTorch 2.x with no legacy dependencies*

**[🚀 Try Browser Demo](https://deoldify.glitch.me/)** • **[📖 GitHub Repo](https://github.com/thookham/DeOldify)** • **[💾 Download Models](#-available-models)**

</div>

---

## ✨ What is DeOldify?

**DeOldify** is a deep learning model that colorizes and restores old black & white images and videos with stunning quality. Created by [Jason Antic](https://github.com/jantic), it uses a novel **NoGAN** training approach that combines the realism of GANs with training stability.

This repository provides:

- ✅ **Modernized inference code** (PyTorch 2.x, Python 3.10+)
- ✅ **No FastAI dependency** (lightweight compatibility layer)
- ✅ **All pretrained weights** (PyTorch .pth + ONNX)
- ✅ **Browser deployment** via ONNX Runtime Web

> **🔗 Sibling Project**: For browser-only deployment, see **[DeOldify-on-Browser](https://huggingface.co/thookham/DeOldify-on-Browser)**

---

## 📦 Available Models

### PyTorch Weights (.pth)

| Model | File | Size | Architecture | Best For |
|-------|------|------|--------------|----------|
| **🎨 Artistic** | `ColorizeArtistic_gen.pth` | ~255 MB | ResNet34 U-Net | Vibrant colors, historical photos |
| **⚖️ Stable** | `ColorizeStable_gen.pth` | ~873 MB | ResNet101 U-Net | Portraits, landscapes, fewer artifacts |
| **🎬 Video** | `ColorizeVideo_gen.pth` | ~873 MB | ResNet101 U-Net | Flicker-free video colorization |

### ONNX Models (Browser/Inference)

| Model | File | Size | Notes |
|-------|------|------|-------|
| **🎨 Artistic** | `deoldify-artistic.onnx` | ~243 MB | Full quality, browser-ready |
| **⚡ Quantized** | `deoldify-quant.onnx` | ~61 MB | 4x smaller, faster inference |

> **📂 All files available in the [Files tab](https://huggingface.co/thookham/DeOldify/tree/main)**

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/thookham/DeOldify.git
cd DeOldify

# Install dependencies
pip install -r requirements.txt
```

### Colorize an Image (Python)

```python
from deoldify.visualize import get_image_colorizer

# Initialize (automatically downloads weights from Hugging Face)
colorizer = get_image_colorizer(artistic=True)

# Colorize from URL
result = colorizer.plot_transformed_image_from_url(
    url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Albert_Einstein%28Nobel%29.png/440px-Albert_Einstein%28Nobel%29.png",
    render_factor=35,
    compare=True
)
print(f"Saved to: {result}")

# Colorize local file
result = colorizer.plot_transformed_image(
    path="./my_photo.jpg",
    render_factor=35
)
```

### Colorize a Video

```python
from deoldify.visualize import get_video_colorizer

colorizer = get_video_colorizer()
result = colorizer.colorize_from_file_name(
    file_name="old_movie.mp4",
    render_factor=21
)
```

### Download Weights Directly

```python
from huggingface_hub import hf_hub_download

# Download Artistic model
model_path = hf_hub_download(
    repo_id="thookham/DeOldify",
    filename="ColorizeArtistic_gen.pth"
)

# Download ONNX model
onnx_path = hf_hub_download(
    repo_id="thookham/DeOldify",
    filename="deoldify-artistic.onnx"
)
```

---

## 🌐 Browser Deployment

For **100% client-side** colorization (no server required), use our ONNX models with ONNX Runtime Web:

- **Live Demo**: [deoldify.glitch.me](https://deoldify.glitch.me/)
- **Full Documentation**: [DeOldify-on-Browser](https://huggingface.co/thookham/DeOldify-on-Browser)

```javascript
// Minimal browser example
import * as ort from 'onnxruntime-web';

const session = await ort.InferenceSession.create(
  'https://huggingface.co/thookham/DeOldify/resolve/main/deoldify-artistic.onnx'
);
```

---

## 🏗️ Architecture

### Model Design

```
Input Image → Grayscale → U-Net Encoder → Self-Attention → U-Net Decoder → RGB Output
                              │                                    │
                         ResNet34/101                         Skip Connections
```

### The NoGAN Advantage

DeOldify's secret sauce is **NoGAN training**—a novel approach that:

1. **Pre-trains** the generator on a perceptual loss (no discriminator)
2. **Brief GAN phase** introduces just enough adversarial training for realism
3. **Result**: Stable training + GAN-quality output without typical artifacts

| Training Approach | Stability | Quality | Artifacts |
|-------------------|-----------|---------|-----------|
| Pure GAN | ❌ Unstable | ⭐⭐⭐⭐⭐ | ❌ Many |
| Pure Perceptual | ✅ Stable | ⭐⭐⭐ | ✅ Few |
| **NoGAN (DeOldify)** | ✅ Stable | ⭐⭐⭐⭐⭐ | ✅ Minimal |

### Training Data

- **Dataset**: ImageNet-1K (subset)
- **Artistic**: 32% of ImageNet, 5 NoGAN cycles
- **Stable**: 7% of ImageNet, 3 NoGAN cycles
- **Video**: 2.2% of ImageNet, 1 cycle (optimized for consistency)

---

## 📋 Model Card

### Model Details

| Attribute | Value |
|-----------|-------|
| **Developer** | Jason Antic (original), Travis Hookham (modernization) |
| **Model Type** | Self-Attention GAN (SAGAN) with U-Net architecture |
| **Language** | Python (PyTorch), JavaScript (ONNX) |
| **License** | MIT |
| **Input** | Grayscale or color images (any resolution) |
| **Output** | RGB colorized images |

### Intended Use

✅ **Recommended Uses**:

- Historical photo restoration
- Black & white film colorization
- Archival media enhancement
- Educational/research purposes
- Creative artistic projects

### Limitations

⚠️ **Known Limitations**:

- Cannot repair physical damage (scratches, tears, stains)
- May produce inaccurate colors for unusual subjects
- Large images require significant memory
- Video colorization is computationally intensive
- Not trained on all historical color palettes

### Ethical Considerations

- Colorization is an **artistic interpretation**, not historical fact
- Consider adding disclaimers when publishing colorized historical content
- Respect copyright and privacy for images of identifiable individuals

---

## 🔗 Related Resources

### Sibling Repositories

| Repository | Purpose | Link |
|------------|---------|------|
| **DeOldify** | PyTorch training & inference | [GitHub](https://github.com/thookham/DeOldify) |
| **DeOldify-on-Browser** | Browser ONNX deployment | [Hugging Face](https://huggingface.co/thookham/DeOldify-on-Browser) |
| **Original DeOldify** | Jason Antic's research repo | [GitHub](https://github.com/jantic/DeOldify) |

### Why DeOldify?

| Feature | DeOldify | Other Colorizers |
|---------|----------|------------------|
| **Quality** | ⭐⭐⭐⭐⭐ State-of-art | ⭐⭐⭐ Variable |
| **Video Support** | ✅ Yes (flicker-free) | ❌ Rare |
| **Browser Ready** | ✅ ONNX included | ❌ Usually not |
| **Modern PyTorch** | ✅ 2.x compatible | ❌ Often legacy |
| **No Dependencies** | ✅ No FastAI | ❌ Often required |

---

## 📚 Citation

If you use DeOldify in your research, please cite the original author:

```bibtex
@misc{antic2019deoldify,
  author = {Antic, Jason},
  title = {DeOldify},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/jantic/DeOldify}}
}
```

---

## 📞 Support

- **🐛 Issues**: [GitHub Issues](https://github.com/thookham/DeOldify/issues)
- **📖 Documentation**: [GitHub Wiki](https://github.com/thookham/DeOldify/wiki)
- **🚀 Browser Demo**: [deoldify.glitch.me](https://deoldify.glitch.me/)

---

<div align="center">

### 🎨 Bringing Color to History

**[Try the Live Demo →](https://deoldify.glitch.me/)**

---

*Modernized with ❤️ by Travis Hookham • Original research by Jason Antic*

</div>
