#!/usr/bin/env bash

if [ -z ${PYTEST_HTML_SPEC+x} ]; then
  echo "ERROR: PYTEST_HTML_SPEC is not defined."
  exit 1
fi

set -eux

# prepare python environment
VENV_PATH="/tmp/merger_venv"
rm -rf $VENV_PATH
python -m venv "${VENV_PATH}"
export VIRTUAL_ENV_DISABLE_PROMPT=1
source "${VENV_PATH}/bin/activate"
pip install bs4 pytest pytest-xdist pytest-rerunfailures

if [ "$PYTEST_HTML_SPEC" = "default" ]; then
  pip install "pytest-html>=4.0.2"
else
  pip install "pytest-html${PYTEST_HTML_SPEC}"
fi

# run builtin tests
python3 -m pytest -l -vvv -n 4 tests

set +eux
