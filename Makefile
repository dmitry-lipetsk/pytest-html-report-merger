PROJECT=pytest_html_report_merger
PYTESTOPTS?=
PYTHON_VERSION?=3.9.11

.PHONY: pyenv
pyenv:
	pyenv install ${PYTHON_VERSION} --skip-existing
	pyenv virtualenv-delete ${PROJECT} || true
	pyenv virtualenv ${PYTHON_VERSION} ${PROJECT}
	pyenv local ${PROJECT}
	pip install poetry
	sed -i '/export VIRTUAL_ENV=/d' .envrc || true
	echo "export VIRTUAL_ENV=\$$$\(pyenv prefix)" >> .envrc
	direnv allow || true
	poetry install

.PHONY: all
all:
	poetry build

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run pytest-html-report-merger \
	    --out data/reports/merged.html \
	    data/reports/report_*.html

.PHONY: test
test:
	poetry run pytest \
	    --verbose \
	    --tb=short \
	    ${PYTESTOPTS}

.PHONY: generate-results
generate-results:
	rm -rf data/reports
	mkdir data/reports
	poetry run pytest \
	    --verbose \
	    --tb=short \
	    -c data/tests/pytest.ini \
	    --html data/reports/report_001.html \
	    -k Set1 \
	    || true
	poetry run pytest \
	    --verbose \
	    --tb=short \
	    -c data/tests/pytest.ini \
	    --html data/reports/report_002.html \
	    -k Set2 \
	    || true
	poetry run pytest \
	    --verbose \
	    --tb=short \
	    -c data/tests/pytest.ini \
	    --html data/reports/report_003.html \
	    -k Set3 \
	    || true
	poetry run pytest \
	    --verbose \
	    --tb=short \
	    -c data/tests/pytest.ini \
	    --html data/reports/report_004.html \
	    -k Set4 \
	    || true


.PHONY: clean
clean:
	find . \( -name '*.pyc' -or -name '*.pyo' \) -print -delete
	find . -name '__pycache__' -print -delete
