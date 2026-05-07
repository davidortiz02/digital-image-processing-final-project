# DeOldify Intel NPU Setup Guide

This guide details how to accelerate DeOldify using the Intel Neural Processing Unit (NPU) found in Intel Core Ultra (Meteor Lake) and newer processors.

## 🚀 Why Use NPU?

* **Efficiency**: NPU is designed for low-power AI inference, saving battery on laptops.
* **Offloading**: Frees up your CPU and GPU for other tasks.
* **Performance**: Optimized for sustained workloads like video colorization.

## 📋 Prerequisites

* **Hardware**: Intel Core Ultra processor (Series 1 or 2) with integrated NPU.
* **OS**: Windows 11 (22H2 or newer).
* **Drivers**: Latest Intel NPU Driver (check Device Manager or Windows Update).

## 🛠️ Installation Steps

### 1. Install Intel OpenVINO Toolkit

DeOldify interacts with the NPU via the OpenVINO toolkit.

```bash
pip install openvino openvino-dev
```

### 2. Install Intel Extension for PyTorch (IPEX)

If you are using the PyTorch backend, you need IPEX to bridge PyTorch models to the NPU.

```bash
pip install intel-extension-for-pytorch
```

### 3. Verify NPU Detection

Run the following Python script to confirm your NPU is visible:

```python
import openvino as ov

core = ov.Core()
devices = core.available_devices

print(f"Available Devices: {devices}")

if "NPU" in devices:
    print("✅ Intel NPU detected!")
else:
    print("❌ NPU not found. Check drivers.")
```

## ⚙️ Configuring DeOldify

To force DeOldify to use the NPU, you typically need to export the model to ONNX or OpenVINO IR format first, as direct PyTorch-to-NPU execution is still experimental.

### Option A: OpenVINO Runtime (Recommended)

1. **Export Model**:

    ```bash
    python export_model.py --model Colorizer --format openvino
    ```

    *(Note: You may need to create this export script if it doesn't exist)*

2. **Run Inference**:
    Set the device to `NPU`.

    ```python
    # In your script
    device = "NPU"
    compiled_model = core.compile_model(model_path, device)
    ```

## 🔍 Troubleshooting

* **"Device NPU not found"**: Update your NPU driver from the device manufacturer's website or Intel.
* **Slow Initialization**: The first run on NPU compiles the model kernels, which can take 1-2 minutes. Subsequent runs will be fast.
* **High RAM Usage**: NPU shares system memory. Ensure you have at least 16GB RAM for 1080p colorization.

## 🔗 Resources

* [Intel NPU Driver Downloads](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html)
* [OpenVINO Documentation](https://docs.openvino.ai/)
