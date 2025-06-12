#!/bin/bash
br //SDK/integration-test/pipelines/python:generate_llm_logits.venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
.SDK+integration-test+pipelines+python+generate_llm_logits.venv/bin/python get-pip.py
rm get-pip.py
.SDK+integration-test+pipelines+python+generate_llm_logits.venv/bin/python -m pip install --upgrade pip debugpy
source .SDK+integration-test+pipelines+python+generate_llm_logits.venv/bin/activate
