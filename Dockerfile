FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir pytest pytest-cov black isort mypy

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/raw_docs data/external_docs

# Production stage
FROM base as production

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/raw_docs data/external_docs

# Expose API and WebSocket ports
EXPOSE 8000

# Set default command
CMD ["python", "api/server.py"] 