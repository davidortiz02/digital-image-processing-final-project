# DeOldify Modernization Roadmap

This document tracks the remaining tasks to fully modernize the DeOldify repository, prioritized by user feedback.

## 🔴 Priority 1: Intel GPU Support (A-1)
*Goal: Ensure robust support for Intel Arc and Data Center GPUs.*

- [x] **Verify `device_id.py`**
    - Ensure `DeviceId` enum includes Intel/XPU options if necessary.
- [x] **Verify Integration**
    - Check if `visualize.py` and other scripts correctly use the `_device.py` manager for Intel hardware.
    - Ensure fallback logic (Intel -> NVIDIA -> CPU) works as intended.
- [ ] **Intel NPU Support**
    - Investigate and implement NPU detection (OpenVINO/IPEX).

## 🔴 Priority 2: NVIDIA GPU Modernization (A-2)
*Goal: Leverage latest CUDA and PyTorch features while maintaining reasonable backward compatibility.*

- [x] **Verify Optimization**
    - Ensure `torch.backends.cudnn.benchmark` and other optimizations are correctly applied for modern NVIDIA GPUs.
    - Double check `environment.yml` against latest PyTorch/CUDA matrix.
- [x] **Legacy CUDA Support**
    - Document support for older drivers (last 5 years) where possible, or provide alternative environment files.

## 🟠 Priority 3: Colab Modernization
*Goal: Fix broken notebooks and improve UX.*

- [x] **Fix `requirements-colab.txt`**
    - Remove `fastai==1.0.60` (conflicts with new PyTorch).
    - Add `torch`, `torchvision`, and other modern dependencies.
- [x] **Update Notebooks**
    - Remove `import fastai`.
    - Use `deoldify.fastai_compat`.
- [x] **UI Improvements**
    - Drag-and-drop, Gallery, Comparison view.

## 🟡 Priority 4: Documentation & Testing
*Goal: Comprehensive guides and stability.*

- [x] **Detailed Documentation**
    - Create `docs/HARDWARE_GUIDE.md` (Benchmarks & Requirements).
    - Create `docs/DEPLOYMENT_GUIDE.md` (Local serving).
- [x] **Testing**
    - Create `tests/` directory with unit tests for device selection and compatibility layer.
    - Add CI/CD workflow.

## 🔵 Future Work: Cloud Integration
- [x] **Migrate Pretrained Weights**
    - Host models on GitHub Releases to ensure longevity.
    - Update all notebooks and docs to point to new URLs.
- [ ] **Google Cloud Platform (Vertex AI)**
    - Deployment scripts and containers.
