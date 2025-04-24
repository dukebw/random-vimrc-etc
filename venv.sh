#!/bin/bash
$MODULAR_PATH/bazelw run //SDK/lib/API/python/max/entrypoints:pipelines.venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.SDK+lib+API+python+max+entrypoints+pipelines.venv/bin/python get-pip.py
.SDK+lib+API+python+max+entrypoints+pipelines.venv/bin/python -m pip install --upgrade --ignore-installed pip python-lsp-server ruff python-lsp-ruff mypy pylsp-mypy pytest pytest-asyncio debugpy py-cpuinfo hypothesis accelerate
rm get-pip.py
fdfind --hidden --no-ignore .bazel .SDK+lib+API+python+max+entrypoints+pipelines.venv | xargs -I {} rm {}
