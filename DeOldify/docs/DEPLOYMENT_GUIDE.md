# DeOldify Deployment Guide

This guide covers the various ways you can deploy and run DeOldify.

## 🏠 Local Deployment

Running DeOldify locally gives you the best performance and privacy, provided you have the necessary hardware.

### Option 1: Conda (Recommended)

We recommend using [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to manage dependencies.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/jantic/DeOldify.git
    cd DeOldify
    ```

2.  **Create the environment**:
    *   **For NVIDIA GPU**:
        ```bash
        conda env create -f environment.yml
        conda activate deoldify
        ```
    *   **For Intel GPU**:
        ```bash
        conda env create -f environment_intel.yml
        conda activate deoldify-intel
        ```

3.  **Run Jupyter Lab**:
    ```bash
    jupyter lab
    ```

### Option 2: Pip

If you prefer standard Python venv:

1.  **Install Python 3.10+**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to install PyTorch manually first to ensure you get the correct CUDA version for your hardware.*

---

## ☁️ Cloud Deployment

### Google Colab

The easiest way to try DeOldify without installing anything.

*   **Image Colorizer**: [Open in Colab](https://colab.research.google.com/github/jantic/DeOldify/blob/master/ImageColorizerColab.ipynb)
*   **Video Colorizer**: [Open in Colab](https://colab.research.google.com/github/jantic/DeOldify/blob/master/VideoColorizerColab.ipynb)

**Notes**:
*   Requires a Google account.
*   Free tier GPUs are sufficient for images and short videos.
*   Pro tier recommended for longer videos or faster rendering.

### Google Cloud Platform (Vertex AI)

*Coming Soon* - We are working on official scripts to deploy DeOldify as a scalable API endpoint on Vertex AI.

### Docker

*Coming Soon* - Official Docker images will be available to simplify deployment on any container orchestration platform.

---

## 📦 Model Weights

DeOldify relies on pre-trained model weights. These are downloaded automatically by the notebooks/scripts when you first run them.

*   **Artistic**: `ColorizeArtistic_gen.pth`
*   **Stable**: `ColorizeStable_gen.pth`
*   **Video**: `ColorizeVideo_gen.pth`

If you are deploying in an air-gapped environment, you will need to download these weights manually and place them in the `models/` directory.
