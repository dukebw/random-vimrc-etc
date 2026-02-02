#!/bin/bash
rm -rf .max+python+max+entrypoints+pipelines.venv/
$MODULAR_PATH/bazelw run //max/python/max/entrypoints:pipelines.venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.max+python+max+entrypoints+pipelines.venv/bin/python get-pip.py
.max+python+max+entrypoints+pipelines.venv/bin/python -m pip install --upgrade --ignore-installed pip python-lsp-server ruff python-lsp-ruff mypy pylsp-mypy pytest pytest-asyncio debugpy pre-commit datasets nvitop matplotlib
rm get-pip.py
# Use fd on macOS, fdfind on Debian/Ubuntu
if command -v fd &> /dev/null; then
  fd --hidden --no-ignore .bazel .max+python+max+entrypoints+pipelines.venv | xargs -I {} rm {}
elif command -v fdfind &> /dev/null; then
  fdfind --hidden --no-ignore .bazel .max+python+max+entrypoints+pipelines.venv | xargs -I {} rm {}
else
  echo "Error: fd/fdfind not found. Install with 'brew install fd' or 'apt install fd-find'"
  exit 1
fi
