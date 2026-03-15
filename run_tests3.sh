#!/usr/bin/env bash

set -eux

# prepare python environment
VENV_PATH="/tmp/merger_venv"
rm -rf $VENV_PATH
python -m venv "${VENV_PATH}"
export VIRTUAL_ENV_DISABLE_PROMPT=1
source "${VENV_PATH}/bin/activate"
pip install -r tests/requirements.txt

# run builtin tests
python3 -m pytest -l -vvv -n 4 tests

set +eux
