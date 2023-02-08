SHELL := bash

.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c 
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

ifeq ($(origin .RECIPEPREFIX), undefined)
	$(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

# Directory Structure
PROJECT_NAME = titanium_white
TEST_DIRECTORY = test

# Virtual Environment
PY = python3
BIN = bin

# Requirements
REQ_DIR = req

all: install lint format test-plan test

.PHONY: install
install:
> $(BIN)/pip install .

.PHONY: test
test: 
> $(PY) -m pytest ./test

.PHONY: test-list
test_list: 
> $(PY) -m pytest --collect-only ./test

.PHONY: test-plan
test_plan: 
> $(PY) -m pytest --setup-plan ./test

.PHONY: lint 
lint: 
> $(BIN)/pylint --exit-zero --jobs 0 --recursive true $(PROJECT_NAME)
> $(BIN)/flake8 --exit-zero --show-source --statistics --benchmark $(PROJECT_NAME)
> $(BIN)/pylint --exit-zero --jobs 0 --recursive true $(TEST_DIRECTORY)
> $(BIN)/flake8 --exit-zero --show-source --statistics --benchmark $(TEST_DIRECTORY)

.PHONY: format 
format: 
> $(BIN)/black --workers 4 --verbose --safe --line-length 100 $(PROJECT_NAME)
> $(BIN)/black --workers 4 --verbose --safe --line-length 100 $(TEST_DIRECTORY)

.PHONY: clean
clean:
> find . -type f -name *.pyc -delete
> find . -type d -name __pycache__ -delete
