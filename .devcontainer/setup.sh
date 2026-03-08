#!/bin/bash
set -e

echo "=== Cleaning Python caches and pip cache ==="
rm -rf ~/.cache/pip
rm -rf ~/.cache/pypoetry
rm -rf ~/.local/share/virtualenvs
pipx install uv
uv sync

# Verify PyTorch installation
python -c "import torch; print('PyTorch version:', torch.__version__)"
