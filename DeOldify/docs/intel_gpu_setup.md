# Intel GPU Setup Guide for DeOldify

This guide covers how to set up DeOldify with Intel GPUs (Arc A-Series, Data Center GPU Max Series) using Intel Extension for PyTorch (IPEX).

## Prerequisites

- **Intel GPU Driver**: Latest stable driver for your hardware.
- **Anaconda** or **Miniconda** installed.
- **Git** installed.
- **OS**: Windows 10/11 or Linux (Ubuntu 22.04 recommended).

## Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/thookham/DeOldify.git
    cd DeOldify
    ```

2.  **Create Intel Conda Environment**
    We use a dedicated environment file that installs PyTorch with XPU support and Intel Extension for PyTorch.
    ```bash
    conda env create -f environment_intel.yml
    ```

3.  **Activate Environment**
    ```bash
    conda activate deoldify_intel
    ```

4.  **Download Weights**
    Download the pretrained weights and place them in the `models/` directory:
    - [ColorizeArtistic_gen.pth](https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeArtistic_gen.pth)
    - [ColorizeStable_gen.pth](https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeStable_gen.pth)
    - [ColorizeVideo_gen.pth](https://github.com/thookham/DeOldify/releases/download/v2.0-models/ColorizeVideo_gen.pth)

## Verification

Run the verification script to ensure your Intel GPU is detected:

```bash
python verify_refactor.py
```

If successful, you should see:
- `Imports successful`
- `Device detection passed`
- `Device Name: Intel(R) Arc(TM)...` (or similar)

## Troubleshooting

### "XPU not available"
- Ensure you have installed the correct drivers.
- Verify that `intel-extension-for-pytorch` is installed: `pip list | grep intel`
- On Windows, ensure you are using the correct oneAPI components if manually installed.

### Performance
- First run might be slower due to JIT compilation.
- Ensure you are using the `deoldify_intel` environment, not the standard one.
