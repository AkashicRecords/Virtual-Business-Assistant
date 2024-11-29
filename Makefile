.PHONY: install test build clean

install:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ --cov=gmail_assistant

build:
	python create_icons.py
	./build.sh

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
