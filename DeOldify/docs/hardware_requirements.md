# Hardware Requirements

DeOldify (Modernized) is designed to run on a variety of hardware configurations. While it can run on a CPU, a dedicated GPU is highly recommended for reasonable performance, especially for video colorization.

## 🖥️ GPU Requirements

### NVIDIA GPUs (Recommended)

The fastest and most supported option.

* **Architecture**: Pascal (10-series) or newer recommended.
* **VRAM**:
  * **Minimum**: 4 GB (Image colorization only)
  * **Recommended**: 8 GB+ (Video colorization, higher resolutions)
  * **Optimal**: 12 GB+ (4K video processing)
* **Drivers**: Latest NVIDIA Studio or Game Ready drivers.
* **CUDA**: Version 11.8 or 12.x.

### Intel GPUs

Supported via Intel Extension for PyTorch (IPEX).

* **Hardware**:
  * Intel Arc A-Series Graphics (A770, A750, A380)
  * Intel Data Center GPU Flex Series
  * Intel Core Ultra (Meteor Lake) integrated Arc graphics
* **VRAM**: 8 GB+ recommended.
* **Software**: Requires `deoldify-intel` environment (see `docs/intel_setup.md`).

### AMD GPUs

*Experimental support via DirectML (Windows) or ROCm (Linux).*

* Currently, AMD support is best achieved via the ONNX Runtime implementation or WSL2 with DirectML. Native ROCm support is planned for a future release.

## 💻 CPU Requirements

If no compatible GPU is found, DeOldify will fall back to CPU mode.

* **Processor**: Modern multi-core processor (Intel Core i5/i7/i9 8th gen+, AMD Ryzen 5/7/9 3000+).
* **Performance**: Expect significantly slower processing times (seconds per image vs milliseconds on GPU). Video colorization will be extremely slow.

## 🧠 System Memory (RAM)

* **Minimum**: 8 GB
* **Recommended**: 16 GB
* **Optimal**: 32 GB+ (Required for processing long videos or batch operations)

## 💾 Storage

* **Disk Space**: ~5 GB for installation (Conda environment + model weights).
* **Type**: SSD recommended for faster model loading and video I/O.
