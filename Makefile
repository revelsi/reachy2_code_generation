.PHONY: setup clean lint install run-gradio check-python create-venv setup-venv install-reachy-sdk refresh-sdk deactivate-venv test

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

deactivate-venv:
	@echo "Cleaning up previous installation..."
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "Removing existing virtual environment: $(VENV_NAME)"; \
		rm -rf $(VENV_NAME); \
	fi
	@echo "Cleaning package installation artifacts..."
	@rm -rf build/ dist/ *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -name "*.pyc" -delete 2>/dev/null
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +

create-venv: check-python deactivate-venv
	@echo "Creating virtual environment with Python $(PYTHON_VERSION)..."
	@if command -v python3.10 >/dev/null 2>&1; then \
		python3.10 -m venv $(VENV_NAME); \
	elif command -v python$(PYTHON_VERSION) >/dev/null 2>&1; then \
		python$(PYTHON_VERSION) -m venv $(VENV_NAME); \
	elif command -v /usr/local/bin/python3.10 >/dev/null 2>&1; then \
		/usr/local/bin/python3.10 -m venv $(VENV_NAME); \
	else \
		echo "Python $(PYTHON_VERSION) not found. Please install Python $(PYTHON_VERSION)."; \
		exit 1; \
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

setup: deactivate-venv check-python create-venv setup-venv
	@echo "Setup complete."
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_NAME)/bin/activate"
	@echo ""
	@echo "NOTE: The environment is NOT automatically activated"

clean:
	@echo "Cleaning generated files and cache..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name "*.so" -delete
	@find . -type d -name "*.o" -delete
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@echo "Clean complete."

lint:
	@. $(VENV_NAME)/bin/activate && flake8 agent/

test:
	@echo "Running code generation tests..."
	@. $(VENV_NAME)/bin/activate && python -m unittest discover tests

install:
	@. $(VENV_NAME)/bin/activate && pip install -e .

run-gradio:
	@. $(VENV_NAME)/bin/activate && python launch_code_gen.py 

refresh-sdk:
	@echo "Refreshing SDK documentation..."
	@. $(VENV_NAME)/bin/activate && python -m agent.utils.refresh_sdk
	@echo "SDK documentation refresh complete!" 