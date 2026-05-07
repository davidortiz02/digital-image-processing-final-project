# NVIDIA GPU Setup Guide for DeOldify

This guide covers how to set up DeOldify with modern NVIDIA GPUs (RTX 30xx, 40xx, 50xx) using CUDA 12.x and PyTorch 2.5+.

## Prerequisites

- **NVIDIA Driver**: Version 550.x or later (supports CUDA 12.4+)
- **Anaconda** or **Miniconda** installed
- **Git** installed

## Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/thookham/DeOldify.git
    cd DeOldify
    ```

2.  **Create Conda Environment**
    We use a modern environment file that installs PyTorch 2.5+ and CUDA 12.4 support.
    ```bash
    conda env create -f environment.yml
    ```

3.  **Activate Environment**
    ```bash
    conda activate deoldify
    ```

4.  **Download Weights**
    Download the pretrained weights and place them in the `models/` directory:
    - [ColorizeArtistic_gen.pth](https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeArtistic_gen.pth)
    - [ColorizeStable_gen.pth](https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeStable_gen.pth)
    - [ColorizeVideo_gen.pth](https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeVideo_gen.pth)

    ```bash
    mkdir -p models
    # Example using wget
    wget https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeArtistic_gen.pth -O models/ColorizeArtistic_gen.pth
    ```

## Verification

Run the verification script to ensure everything is set up correctly:

```bash
python verify_refactor.py
```

## Troubleshooting

### "CUDA not available"
- Ensure you have the correct NVIDIA drivers installed.
- Run `nvidia-smi` to check driver status.
- Ensure you installed the environment from `environment.yml` which pulls `pytorch-cuda`.

### "Out of Memory"
- Reduce `render_factor` in your scripts.
- Ensure no other processes are using the GPU.

### Performance Tuning
- For RTX 40xx/50xx series, you can enable TF32 for better performance:
  ```python
  import torch
  torch.backends.cuda.matmul.allow_tf32 = True
  torch.backends.cudnn.allow_tf32 = True
  ```
