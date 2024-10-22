#!/bin/bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.SDK+public+max-repo+pipelines+python+pipelines.venv/bin/python get-pip.py
.SDK+public+max-repo+pipelines+python+pipelines.venv/bin/python -m pip install --upgrade pip python-lsp-server ruff python-lsp-ruff mypy pylsp-mypy pytest
rm get-pip.py
