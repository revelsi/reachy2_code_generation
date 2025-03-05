.PHONY: setup clean test lint install run-cli run-web check-python create-venv setup-venv regenerate generate-tools refresh-sdk test-virtual demo-virtual test-agent test-unit test-integration install-reachy-sdk

PYTHON_VERSION := 3.10
VENV_NAME := venv_py310

check-python:
	@echo "Checking for Python $(PYTHON_VERSION)..."
	@if command -v python3.10 >/dev/null 2>&1; then \
		PYTHON_CMD="python3.10"; \
	elif command -v python$(PYTHON_VERSION) >/dev/null 2>&1; then \
		PYTHON_CMD="python$(PYTHON_VERSION)"; \
	elif command -v /usr/local/bin/python3.10 >/dev/null 2>&1; then \
		PYTHON_CMD="/usr/local/bin/python3.10"; \
	else \
		echo "Python $(PYTHON_VERSION) not found. Please install Python $(PYTHON_VERSION)."; \
		exit 1; \
	fi; \
	$$PYTHON_CMD --version

create-venv: check-python
	@echo "Creating virtual environment with Python $(PYTHON_VERSION)..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		if command -v python3.10 >/dev/null 2>&1; then \
			python3.10 -m venv $(VENV_NAME); \
		elif command -v python$(PYTHON_VERSION) >/dev/null 2>&1; then \
			python$(PYTHON_VERSION) -m venv $(VENV_NAME); \
		elif command -v /usr/local/bin/python3.10 >/dev/null 2>&1; then \
			/usr/local/bin/python3.10 -m venv $(VENV_NAME); \
		else \
			echo "Python $(PYTHON_VERSION) not found. Please install Python $(PYTHON_VERSION)."; \
			exit 1; \
		fi; \
	else \
		echo "Virtual environment $(VENV_NAME) already exists."; \
	fi

setup-venv: create-venv
	@echo "Installing dependencies in virtual environment..."
	@. $(VENV_NAME)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@$(MAKE) install-reachy-sdk

install-reachy-sdk:
	@echo "Installing Reachy2 SDK in editable mode..."
	@. $(VENV_NAME)/bin/activate && pip install reachy2-sdk -e . || \
		(echo "Warning: Failed to install Reachy2 SDK in editable mode. Some functionality may be limited."; \
		echo "You may need to manually install it later with: pip install reachy2-sdk -e .")

setup: setup-venv
	@echo "Setup complete. Activate the virtual environment with: source $(VENV_NAME)/bin/activate"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

test: test-unit test-integration
	@echo "All tests completed."

test-unit:
	@echo "Running unit tests..."
	@. $(VENV_NAME)/bin/activate && pytest tests/unit/ -v

test-integration:
	@echo "Running integration tests..."
	@. $(VENV_NAME)/bin/activate && pytest tests/integration/ tests/test_agent_integration.py -v

lint:
	@. $(VENV_NAME)/bin/activate && flake8 agent/ agent/utils/scrape_sdk_docs.py

install:
	@. $(VENV_NAME)/bin/activate && pip install -e .

run-cli:
	@. $(VENV_NAME)/bin/activate && python agent/cli.py

run-web:
	@. $(VENV_NAME)/bin/activate && python agent/web_interface.py

test-virtual:
	@echo "Running virtual Reachy tests..."
	@. $(VENV_NAME)/bin/activate && python tests/integration/test_virtual_reachy.py

demo-virtual:
	@echo "Starting virtual Reachy demo..."
	@. $(VENV_NAME)/bin/activate && python demo_virtual_reachy.py

regenerate:
	@. $(VENV_NAME)/bin/activate && python agent/utils/scrape_sdk_docs.py 

refresh-sdk:
	@echo "Refreshing SDK documentation by pulling latest SDK repository..."
	@. $(VENV_NAME)/bin/activate && python -m agent.utils.refresh_sdk
	@echo "SDK documentation refreshed. Now regenerating tools..."
	@$(MAKE) generate-tools

generate-tools:
	@echo "Generating tools from API documentation..."
	@mkdir -p agent/docs
	@echo "Copying API documentation..."
	@cp data/raw_docs/extracted/raw_api_docs.json agent/docs/api_documentation.json
	@. $(VENV_NAME)/bin/activate && python -m agent.utils.integrate_tools
	@echo "Tool generation completed."

test-agent:
	python tests/test_agent.py -v 