#!/usr/bin/env python
"""
Configuration settings for the Reachy Function Calling project.
This file centralizes configuration settings and provides defaults.
"""

import os
import sys
import platform
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional

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

# Model settings
MODEL = os.getenv("MODEL", "gpt-4.1")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "gpt-4.1-mini")  # Default model for code evaluation
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
MODEL_MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "4000"))
MODEL_TOP_P = float(os.getenv("MODEL_TOP_P", "0.95"))
MODEL_FREQUENCY_PENALTY = float(os.getenv("MODEL_FREQUENCY_PENALTY", "0"))
MODEL_PRESENCE_PENALTY = float(os.getenv("MODEL_PRESENCE_PENALTY", "0"))

# Model configuration dictionary for easy access
MODEL_CONFIG = {
    "model": MODEL,
    "evaluator_model": EVALUATOR_MODEL,
    "temperature": MODEL_TEMPERATURE,
    "max_tokens": MODEL_MAX_TOKENS,
    "top_p": MODEL_TOP_P,
    "frequency_penalty": MODEL_FREQUENCY_PENALTY,
    "presence_penalty": MODEL_PRESENCE_PENALTY,
}

# Available models for selection in UI
AVAILABLE_MODELS = [
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
]

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
# Note: When REACHY_HOST is set to "localhost", we connect to a robot running in a Docker container.
# Otherwise, we connect to a physical robot at the specified IP address.

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

def get_model_config() -> Dict[str, Any]:
    """
    Get the current model configuration.
    
    Returns:
        Dict[str, Any]: The model configuration.
    """
    return MODEL_CONFIG.copy()

def update_model_config(config: Dict[str, Any]) -> None:
    """
    Update the model configuration.
    
    Args:
        config: The new model configuration.
    """
    global MODEL, MODEL_TEMPERATURE, MODEL_MAX_TOKENS, MODEL_TOP_P
    global MODEL_FREQUENCY_PENALTY, MODEL_PRESENCE_PENALTY, MODEL_CONFIG
    
    # Update global variables
    if "model" in config:
        MODEL = config["model"]
    if "evaluator_model" in config:
        EVALUATOR_MODEL = config["evaluator_model"]
    if "temperature" in config:
        MODEL_TEMPERATURE = float(config["temperature"])
    if "max_tokens" in config:
        MODEL_MAX_TOKENS = int(config["max_tokens"])
    if "top_p" in config:
        MODEL_TOP_P = float(config["top_p"])
    if "frequency_penalty" in config:
        MODEL_FREQUENCY_PENALTY = float(config["frequency_penalty"])
    if "presence_penalty" in config:
        MODEL_PRESENCE_PENALTY = float(config["presence_penalty"])
    
    # Update the model configuration dictionary
    MODEL_CONFIG = {
        "model": MODEL,
        "evaluator_model": EVALUATOR_MODEL,
        "temperature": MODEL_TEMPERATURE,
        "max_tokens": MODEL_MAX_TOKENS,
        "top_p": MODEL_TOP_P,
        "frequency_penalty": MODEL_FREQUENCY_PENALTY,
        "presence_penalty": MODEL_PRESENCE_PENALTY,
    } 