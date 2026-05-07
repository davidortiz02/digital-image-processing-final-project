# DeOldify Hardware Compatibility Guide

This guide outlines the supported hardware configurations for running DeOldify. We support a wide range of devices, from consumer GPUs to data center accelerators and CPUs.

## 🚀 Quick Reference Matrix

| Hardware Type | Supported Devices | Recommended VRAM | Setup Guide |
| :--- | :--- | :--- | :--- |
| **NVIDIA GPU** | GeForce GTX 10-series+, RTX 20/30/40-series, Tesla, A100/H100 | 4GB+ (8GB+ for Video) | [NVIDIA Setup](nvidia_setup.md) |
| **Intel GPU** | Arc A-Series (A770, A750), Data Center GPU Flex/Max | 8GB+ | [Intel Setup](intel_gpu_setup.md) |
| **CPU** | Any modern x86_64 CPU (Intel/AMD) | N/A (System RAM > 16GB) | Standard Installation |

---

## 🟢 NVIDIA GPUs (Recommended)

NVIDIA GPUs provide the most mature ecosystem for Deep Learning. DeOldify is optimized to take advantage of CUDA cores and Tensor cores on modern NVIDIA hardware.

### Requirements
*   **Driver**: CUDA-compatible driver (ensure support for CUDA 11.8 or 12.x).
*   **VRAM**:
    *   **Artistic Images**: Minimum 4GB.
    *   **Stable Video**: Minimum 8GB recommended to handle frame buffering and larger batch sizes.
*   **Performance**: `torch.backends.cudnn.benchmark` is enabled by default to optimize performance on your specific card.

### Legacy Support
We strive to support NVIDIA drivers released in the last 5 years. If you are on an older GPU (e.g., Maxwell/Pascal architecture) that does not support CUDA 12.x:
1.  Ensure your driver supports at least CUDA 11.8.
2.  Use the legacy environment file:
    ```bash
    conda env create -f environment-legacy.yml
    conda activate deoldify-legacy
    ```

---

## 🔵 Intel GPUs (New!)

We now support Intel's discrete GPUs, including the Arc A-Series and Data Center GPU Flex/Max series, via the **Intel® Extension for PyTorch (IPEX)**.

### Requirements
*   **Hardware**: Intel Arc A750, A770, or Data Center GPU Flex/Max Series.
*   **Software**: Intel® Graphics Driver (latest stable release).
*   **Environment**: Requires a specific Conda environment (see setup guide).

### Performance Notes
*   **XPU Acceleration**: DeOldify automatically detects Intel GPUs as `xpu` devices.
*   **Memory**: Intel Arc cards with 16GB VRAM (like the A770 16GB) are excellent for high-resolution video colorization.

---

## ⚪ CPU (Fallback)

If no GPU is detected, DeOldify will fallback to CPU mode.

### Pros & Cons
*   **Pros**: Works on almost any computer. No complex driver setup.
*   **Cons**: Significantly slower than GPU. Video colorization may be impractical for long clips.
*   **Recommendation**: Use for testing or single image colorization if no GPU is available.

---

## 📊 Benchmarks (Estimated)

| Task | RTX 4090 | Arc A770 | CPU (Core i9) |
| :--- | :--- | :--- | :--- |
| **Image (Artistic)** | < 1 sec | ~2 sec | ~10-20 sec |
| **Video (1 min, 1080p)** | ~2 mins | ~4 mins | ~30+ mins |

*Note: Benchmarks are approximate and depend on render factor and resolution.*
