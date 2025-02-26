.PHONY: setup clean test lint install run-cli run-web

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

test:
	pytest agent/test_*.py

lint:
	flake8 agent/ agent/tools/scrape_sdk_docs.py

install:
	pip install -e .

run-cli:
	python agent/cli.py

run-web:
	python agent/web_interface.py

regenerate:
	python agent/tools/scrape_sdk_docs.py 