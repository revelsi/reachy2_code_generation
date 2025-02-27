.PHONY: setup clean test lint install run-cli run-web check-python create-venv setup-venv regenerate generate-tools

PYTHON_VERSION := 3.10
VENV_NAME := venv_py310

check-python:
	@echo "Checking Python version..."
	@python3 -c "import sys; v=sys.version_info; sys.exit(0 if v.major==3 and v.minor>=10 else 1)" || \
		(echo "Python 3.10+ is required. Current version: $$(python3 --version)"; exit 1)

create-venv: check-python
	@echo "Creating virtual environment with Python $(PYTHON_VERSION)..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		python3 -m venv $(VENV_NAME); \
	else \
		echo "Virtual environment $(VENV_NAME) already exists."; \
	fi

setup-venv: create-venv
	@echo "Installing dependencies in virtual environment..."
	@. $(VENV_NAME)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

setup: setup-venv
	@echo "Setup complete. Activate the virtual environment with: source $(VENV_NAME)/bin/activate"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

test:
	@. $(VENV_NAME)/bin/activate && pytest agent/test_*.py

lint:
	@. $(VENV_NAME)/bin/activate && flake8 agent/ agent/tools/scrape_sdk_docs.py

install:
	@. $(VENV_NAME)/bin/activate && pip install -e .

run-cli:
	@. $(VENV_NAME)/bin/activate && python agent/cli.py

run-web:
	@. $(VENV_NAME)/bin/activate && python agent/web_interface.py

regenerate:
	@. $(VENV_NAME)/bin/activate && python agent/tools/scrape_sdk_docs.py 

generate-tools:
	@echo "Generating tools from API documentation..."
	@mkdir -p agent/docs
	@if [ ! -f "agent/docs/api_documentation.json" ]; then \
		echo "Copying API documentation..."; \
		cp data/raw_docs/extracted/raw_api_docs.json agent/docs/api_documentation.json; \
	fi
	@. $(VENV_NAME)/bin/activate && python -m agent.utils.integrate_tools
	@echo "Tool generation completed." 