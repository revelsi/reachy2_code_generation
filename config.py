#!/usr/bin/env python
"""
Configuration settings for the Reachy Function Calling project.
This file centralizes configuration settings and provides defaults.
"""

import os
import sys
import platform
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Python version check
REQUIRED_PYTHON_VERSION = (3, 10)
current_version = sys.version_info[:2]
if current_version < REQUIRED_PYTHON_VERSION:
    print(f"Error: Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}+ is required.")
    print(f"Current version: {sys.version}")
    sys.exit(1)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TOOLS_DIR = os.path.join(BASE_DIR, "agent", "tools")

# Network settings
HTTP_PROXY = os.getenv("HTTP_PROXY", "")
HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")

# If proxies are set, configure them
PROXIES = {}
if HTTP_PROXY:
    PROXIES["http://"] = HTTP_PROXY
if HTTPS_PROXY:
    PROXIES["https://"] = HTTPS_PROXY

# Environment settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("MODEL", "gpt-4-turbo")
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))

# WebSocket settings
WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
WS_PORT = int(os.getenv("WS_PORT", "8765"))
DISABLE_WEBSOCKET = os.getenv("DISABLE_WEBSOCKET", "false").lower() in ("true", "1", "t")

# Robot settings
REACHY_HOST = os.getenv("REACHY_HOST", "localhost")
USE_MOCK = os.getenv("USE_MOCK", "true").lower() in ("true", "1", "t")
USE_VIRTUAL = os.getenv("USE_VIRTUAL", "true").lower() in ("true", "1", "t")

# System information
SYSTEM_INFO = {
    "os": platform.system(),
    "os_version": platform.version(),
    "python_version": platform.python_version(),
    "platform": platform.platform(),
}

# Print configuration in debug mode
if DEBUG:
    print("Configuration:")
    print(f"- Python version: {platform.python_version()}")
    print(f"- Operating system: {platform.system()} {platform.version()}")
    print(f"- Base directory: {BASE_DIR}")
    print(f"- OpenAI API key: {'Set' if OPENAI_API_KEY else 'Not set'}")
    print(f"- Model: {MODEL}")
    print(f"- API: {API_HOST}:{API_PORT}")
    print(f"- WebSocket: {'Disabled' if DISABLE_WEBSOCKET else f'{WS_HOST}:{WS_PORT}'}")
    print(f"- Reachy host: {REACHY_HOST}")
    print(f"- Use mock: {USE_MOCK}")
    print(f"- Use virtual: {USE_VIRTUAL}") 