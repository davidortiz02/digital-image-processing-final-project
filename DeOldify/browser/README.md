# DeOldify Browser Integration

This directory contains a browser-based implementation of DeOldify using ONNX Runtime Web. It allows you to run colorization models directly in your web browser without a backend server (after the model is downloaded).

## ⚠️ Important: How to Run

Due to browser security policies (CORS), **you cannot simply double-click the HTML files** to run them. You must serve them via a local HTTP server.

### Quick Start (Windows/Linux/Mac)

If you have Python installed (which is likely if you're using DeOldify), simply run:

```bash
# Run this command in your terminal within this directory
python -m http.server 8000
```

Then open your browser and visit:
*   [http://localhost:8000](http://localhost:8000)

### Using the Helper Script (Windows)

We've provided a PowerShell script to make this easy:

1.  Right-click `serve.ps1` and select "Run with PowerShell"
2.  Or run it from the terminal: `.\serve.ps1`

## Available Models

*   **Artistic Model**: High quality, vibrant colors. Larger download (~243 MB).
*   **Quantized Model**: Faster, smaller download (~61 MB), slightly lower quality.

## Troubleshooting

**"Failed to fetch" or CORS Errors:**
If you see an error about CORS or "Failed to fetch" in the status log, it means you are likely trying to open the file directly (`file:///...`). Please use the HTTP server method described above.

**Memory Issues:**
The artistic model requires a significant amount of RAM. If the tab crashes, try closing other tabs or using the Quantized model.
