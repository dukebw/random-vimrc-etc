#!/bin/bash
rm -rf .max+python+max+entrypoints+pipelines.venv/
$MODULAR_PATH/bazelw run //maxpython/max/entrypoints:pipelines.venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.max+python+max+entrypoints+pipelines.venv/bin/python get-pip.py
.max+python+max+entrypoints+pipelines.venv/bin/python -m pip install --upgrade --ignore-installed pip python-lsp-server ruff python-lsp-ruff mypy pylsp-mypy pytest pytest-asyncio debugpy pre-commit datasets nvitop matplotlib
rm get-pip.py
fdfind --hidden --no-ignore .bazel .max+python+max+entrypoints+pipelines.venv | xargs -I {} rm {}
