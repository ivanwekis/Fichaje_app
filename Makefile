PROJECT_NAME = $(notdir ${PWD})
# Convert to lowercase
PROJECT_NAME := $(shell echo ${PROJECT_NAME} | tr A-Z a-z)

ENV ?= dev
export ENV

# Load environment variable for functional test
NAMESPACE ?= local
export NAMESPACE

# Enable flask debug (hot reload with file changes)
FLASK_ENV ?= development

TARGET_TEST=$(if ${TEST},${TEST},tests/)
COV=$(if ${TEST},,--cov=app --cov-report=term --cov-report=xml:coverage.xml --junitxml=report.xml)
TARGET_FUNCTIONAL_TEST=$(if ${FUNCTIONAL_TEST},${FUNCTIONAL_TEST},functional_tests/)


help:
	@echo
	@echo "help"
	@echo "       Print this help"
	@echo

	@echo "init"
	@echo "       Initialise dependencies to test and run the application."
	@echo

	@echo "check"
	@echo "       Run static analysis"
	@echo

	@echo "test"
	@echo "       Run unit tests with coverage. \
	Use TEST=/path/to/test to run a specific test."
	@echo

	@echo "run"
	@echo "       Run the application. \
	@echo

	@echo "build"
	@echo "       Build docker image. \
	@echo

	@echo "functional_test"
	@echo "       Run functional tests. \
	@echo

init:
	@python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.txt && deactivate

check:
	@source .venv/bin/activate && python3 -m flake8 app/ ${TARGET_TEST} ${TARGET_FUNCTIONAL_TEST} && deactivate

build:
	@docker build . -t ${PROJECT_NAME}-${ENV} 

test:
	@source .venv/bin/activate && pytest ${COV} ${TARGET_TEST} && deactivate

functional_test:
	@source .venv/bin/activate && pytest ${TARGET_FUNCTIONAL_TEST} && deactivate

run:
	@source .venv/bin/activate && uvicorn app.main:app --reload && deactivate
