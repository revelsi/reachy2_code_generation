FROM python:3.10-slim

WORKDIR /app

# Install git for cloning the SDK repository
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create data directories
RUN mkdir -p data/raw_docs data/external_docs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command to run the web interface
CMD ["python", "agent/web_interface.py", "--share"]

# Expose the port that Gradio uses
EXPOSE 7860 