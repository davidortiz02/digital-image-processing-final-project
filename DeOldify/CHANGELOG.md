# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-12-01

### Added
- **Intel GPU Support**: Added support for Intel Arc and Data Center GPUs using Intel Extension for PyTorch (IPEX).
- **Unified Device Management**: Implemented `deoldify.device` to automatically detect and manage CUDA, XPU (Intel), and CPU devices.
- **Documentation**:
    - `docs/nvidia_setup.md`: Comprehensive guide for setting up NVIDIA GPUs with CUDA 12.x.
    - `docs/intel_gpu_setup.md`: Guide for setting up Intel GPUs.
- **Verification Script**: Added `verify_refactor.py` to validate environment setup and model instantiation.
- **Compatibility Layer**: Created `deoldify/fastai_compat.py` to replace the obsolete `fastai` 1.x library, ensuring compatibility with modern PyTorch.
- **Requirements Files**: Added `requirements.txt` and `requirements_intel.txt` for pip users.
- **Code Quality**:
    - Comprehensive module docstring for `fastai_compat.py`.
    - Type hints throughout compatibility layer.
    - README badges for Python, PyTorch, CUDA versions, and license.

### Changed
- **Core Dependencies**:
    - Removed dependency on `fastai` 1.x.
    - Upgraded PyTorch to 2.5+.
    - Upgraded CUDA support to 12.x.
    - Updated `environment.yml` for modern NVIDIA environments.
    - Created `environment_intel.yml` for Intel environments.
- **Refactoring**:
    - Refactored `visualize.py`, `filters.py`, `generators.py`, `unet.py`, and `layers.py` to use pure PyTorch and the new compatibility layer.
    - Replaced FastAI-specific image processing with standard `torchvision` transforms.
- **Device Handling**: Updated `Learner` and `DataBunch` shims to use the new unified device manager.
- **.gitignore**: Enhanced to exclude model weights in `models/` directory, logs, IDE files, and OS-specific files.

### Removed
- **Legacy Code**: Removed direct imports of `fastai` throughout the codebase.
- **Archived Status**: The project is now actively maintained for modern hardware.
