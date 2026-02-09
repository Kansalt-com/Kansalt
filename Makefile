.PHONY: help install run run-docker docker-build docker-clean test clean setup

help:
	@echo "Kansalt - Job Aggregator Portal"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make install       - Install dependencies"
	@echo "  make setup         - Run initial setup"
	@echo "  make run           - Run Streamlit app locally"
	@echo "  make run-docker    - Run with Docker Compose"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-clean  - Remove Docker containers/images"
	@echo "  make clean         - Clean Python cache"
	@echo "  make test          - Run tests"
	@echo ""

install:
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

setup:
	python setup.py
	@echo "✓ Setup complete"

run:
	streamlit run app/main.py --server.port 8501

run-docker:
	docker-compose up --build

docker-build:
	docker build -t kansalt:latest .
	@echo "✓ Docker image built"

docker-clean:
	docker-compose down
	docker system prune -f
	@echo "✓ Docker cleaned"

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cache cleaned"
