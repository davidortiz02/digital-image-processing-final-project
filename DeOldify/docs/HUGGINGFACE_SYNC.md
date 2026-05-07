# HuggingFace Sync

This repository automatically syncs to HuggingFace on every push to the `main` branch via GitHub Actions.

## Overview

| GitHub Repository | HuggingFace Repository | Models |
|------------------|----------------------|--------|
| [thookham/DeOldify](https://github.com/thookham/DeOldify) | [thookham/DeOldify](https://huggingface.co/thookham/DeOldify) | PyTorch + ONNX |
| [thookham/DeOldify-on-Browser](https://github.com/thookham/DeOldify-on-Browser) | [thookham/DeOldify-on-Browser](https://huggingface.co/thookham/DeOldify-on-Browser) | ONNX only |

## How It Works

1. **Push to main** → GitHub Action triggers
2. **Workflow runs** → Pushes code to HuggingFace
3. **HuggingFace updates** → Models/code available

## Setup Requirements

### 1. Create HuggingFace Token

1. Go to [HuggingFace Settings → Access Tokens](https://huggingface.co/settings/tokens)
2. Create new token with **Write** permissions
3. Copy the token (starts with `hf_...`)

### 2. Add GitHub Secret

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `HF_TOKEN`
4. Value: Your HuggingFace token

## Manual Sync

If you need to sync manually:

```bash
# Add HuggingFace remote (if not exists)
git remote add hf https://huggingface.co/thookham/DeOldify

# Push to HuggingFace
git push hf main --force
```

## Verification

Run the verification script to check sync status:

```powershell
.\scripts\verify-hf-sync.ps1
```

## Troubleshooting

**"Permission denied" error:**

- Ensure `HF_TOKEN` secret is set correctly
- Verify token has write permissions

**"Remote already exists" error:**

- This is normal, the workflow handles this case

**Workflow not triggering:**

- Ensure you're pushing to `main` branch
- Check GitHub Actions tab for workflow status
