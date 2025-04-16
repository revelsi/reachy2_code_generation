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

# --- Model Selection ---
# Model names are read from environment variables (e.g., set in .env file).
# The values in .env will override the defaults specified here.
_MODEL_NAME = os.getenv("MODEL", "gpt-4.1-mini")
_EVALUATOR_MODEL_NAME = os.getenv("EVALUATOR_MODEL", "gpt-4.1-nano")

# --- Model Parameter Templates ---
# Define default parameter sets for different model families.

# Default parameters for standard GPT models
_GPT_DEFAULT_PARAMS = {
    "temperature": float(os.getenv("MODEL_TEMPERATURE", "0.2")),
    "max_tokens": int(os.getenv("MODEL_MAX_TOKENS", "4000")),
    "top_p": float(os.getenv("MODEL_TOP_P", "0.95")),
    "frequency_penalty": float(os.getenv("MODEL_FREQUENCY_PENALTY", "0")),
    "presence_penalty": float(os.getenv("MODEL_PRESENCE_PENALTY", "0")),
}

# Default parameters for O-family models (o1, o3, etc.)
# Based on search results and API errors, these support specific params.
_O_FAMILY_DEFAULT_PARAMS = {
    # "temperature": float(os.getenv("MODEL_TEMPERATURE", "0.3")), # REMOVED: Not supported by o3-mini
    # O-family uses 'max_completion_tokens' instead of 'max_tokens'
    "max_completion_tokens": int(os.getenv("MODEL_MAX_COMPLETION_TOKENS", "4000")), 
    "reasoning_effort": os.getenv("MODEL_REASONING_EFFORT", "medium"), # low, medium, high
}

# Available models for selection in UI or validation
AVAILABLE_MODELS = [
    # GPT Family
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano",
    "gpt-4o", "gpt-4o-mini",
    "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo",
    # O-Family (Reasoning focused)
    "o1", "o1-mini", "o3", "o3-mini",
]

# Mapping or logic to determine model family and get parameters
def _get_params_for_model(model_name: str) -> Dict[str, Any]:
    """Returns a copy of the default parameters for the given model's family."""
    model_name_lower = model_name.lower()
    # Simple check based on model name prefix/content. Adjust as needed.
    if model_name_lower.startswith("gpt-"):
        return _GPT_DEFAULT_PARAMS.copy()
    elif model_name_lower.startswith("o1") or model_name_lower.startswith("o3"):
        return _O_FAMILY_DEFAULT_PARAMS.copy()
    else:
        # Fallback: Use GPT defaults if family is unrecognized
        print(f"Warning: Unrecognized model family for '{model_name}'. Falling back to GPT default parameters.", file=sys.stderr)
        return _GPT_DEFAULT_PARAMS.copy()

# --- Active Model Configuration Initialization ---

# Validate the primary model name
if _MODEL_NAME not in AVAILABLE_MODELS:
     print(f"Warning: Configured MODEL '{_MODEL_NAME}' is not in AVAILABLE_MODELS list. Behavior might be unpredictable.", file=sys.stderr)

# Initialize the active configuration based on the primary model
MODEL_CONFIG = _get_params_for_model(_MODEL_NAME)
MODEL_CONFIG["model"] = _MODEL_NAME

# Handle evaluator model configuration
# For simplicity, evaluator also uses parameters based on its own family.
# Consider if evaluator needs a separate config structure if its usage differs significantly.
if _EVALUATOR_MODEL_NAME not in AVAILABLE_MODELS:
     print(f"Warning: Configured EVALUATOR_MODEL '{_EVALUATOR_MODEL_NAME}' is not in AVAILABLE_MODELS list.", file=sys.stderr)

_EVALUATOR_PARAMS = _get_params_for_model(_EVALUATOR_MODEL_NAME)
MODEL_CONFIG["evaluator_model"] = _EVALUATOR_MODEL_NAME
# Store evaluator-specific params distinctly if needed, e.g.:
# MODEL_CONFIG["evaluator_params"] = _EVALUATOR_PARAMS


# --- Deprecated Global Variables (for potential backward compatibility) ---
# Direct use is discouraged. Use get_model_config() instead.
MODEL = _MODEL_NAME
EVALUATOR_MODEL = _EVALUATOR_MODEL_NAME
# These will reflect the primary model's config. Access via MODEL_CONFIG is preferred.
MODEL_TEMPERATURE = MODEL_CONFIG.get("temperature")
MODEL_MAX_TOKENS = MODEL_CONFIG.get("max_tokens")
MODEL_TOP_P = MODEL_CONFIG.get("top_p")
MODEL_FREQUENCY_PENALTY = MODEL_CONFIG.get("frequency_penalty")
MODEL_PRESENCE_PENALTY = MODEL_CONFIG.get("presence_penalty")
MODEL_REASONING_EFFORT = MODEL_CONFIG.get("reasoning_effort")
MODEL_MAX_COMPLETION_TOKENS = MODEL_CONFIG.get("max_completion_tokens")

# --- Rest of the file ---
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
    print("--- Configuration ---")
    print(f"- Python version: {SYSTEM_INFO['python_version']}")
    print(f"- OS: {SYSTEM_INFO['os']} {SYSTEM_INFO['os_version']}")
    print(f"- Base directory: {BASE_DIR}")
    print(f"- OpenAI API key: {'Set' if OPENAI_API_KEY else 'Not set'}")
    print(f"- API: {API_HOST}:{API_PORT}")
    print(f"- WebSocket: {'Disabled' if DISABLE_WEBSOCKET else f'{WS_HOST}:{WS_PORT}'}")
    print(f"- Reachy host: {REACHY_HOST}")
    print(f"- Primary Model: {MODEL_CONFIG.get('model')}")
    print(f"- Evaluator Model: {MODEL_CONFIG.get('evaluator_model')}")
    # Extract and print only the parameters for the primary model
    active_params = {k: v for k, v in MODEL_CONFIG.items() if k not in ['model', 'evaluator_model', 'evaluator_params']}
    print(f"- Active Model Params: {active_params}")
    print("--- End Configuration ---")


def get_model_config() -> Dict[str, Any]:
    """
    Get the current model configuration for the primary model.

    Returns:
        Dict[str, Any]: The active model configuration dictionary, containing
                        'model' name and its specific parameters.
    """
    # Return only the primary model name and its relevant parameters
    # Exclude evaluator info from this specific getter for clarity
    config_copy = MODEL_CONFIG.copy()
    config_copy.pop("evaluator_model", None)
    # config_copy.pop("evaluator_params", None) # If evaluator_params were added
    return config_copy

def update_model_config(config: Dict[str, Any]) -> None:
    """
    Update the primary model configuration.
    Handles updates potentially changing the model family and its associated parameters.

    Args:
        config: The new configuration settings. Can include 'model' and
                specific parameters like 'temperature', 'max_tokens', 'reasoning_effort', etc.
                Updates apply only to the primary model configuration.
    """
    global MODEL_CONFIG, MODEL
    global MODEL_TEMPERATURE, MODEL_MAX_TOKENS, MODEL_TOP_P, MODEL_FREQUENCY_PENALTY, MODEL_PRESENCE_PENALTY, MODEL_REASONING_EFFORT
    global MODEL_MAX_COMPLETION_TOKENS

    current_model_name = MODEL_CONFIG.get("model")
    new_model_name = config.get("model", current_model_name)

    # If the model name changes, re-initialize the config based on the new family
    if new_model_name != current_model_name:
        if new_model_name not in AVAILABLE_MODELS:
            print(f"Warning: Attempting to switch to model '{new_model_name}' which is not in AVAILABLE_MODELS.", file=sys.stderr)
            # Optionally prevent the switch or allow it with a warning
            # For now, allow switch but use fallback params if needed
            # return # Or raise an error?

        print(f"Switching primary model from '{current_model_name}' to '{new_model_name}'")
        new_params = _get_params_for_model(new_model_name)
        
        # Preserve evaluator info, replace only model name and its params
        evaluator_model = MODEL_CONFIG.get("evaluator_model")
        # evaluator_params = MODEL_CONFIG.get("evaluator_params") # If using separate evaluator params

        MODEL_CONFIG = new_params # Start with new defaults
        MODEL_CONFIG["model"] = new_model_name
        MODEL_CONFIG["evaluator_model"] = evaluator_model # Put evaluator back
        # if evaluator_params: MODEL_CONFIG["evaluator_params"] = evaluator_params

        MODEL = new_model_name # Update global MODEL name

    # Update specific parameters present in the incoming config *and* relevant
    # to the *current* model family (potentially after a switch)
    current_param_keys = set(MODEL_CONFIG.keys()) - {"model", "evaluator_model", "evaluator_params"}
    
    for key, value in config.items():
        if key == "model": # Already handled above
            continue
        if key == "evaluator_model": # Not handled by this function
             print(f"Warning: 'evaluator_model' update ignored by update_model_config. Use a dedicated function if needed.", file=sys.stderr)
             continue

        if key in current_param_keys:
            expected_type = type(MODEL_CONFIG[key])
            try:
                # Attempt type conversion based on the default type
                converted_value = expected_type(value)
                MODEL_CONFIG[key] = converted_value
                # Update specific global vars if necessary
                if key == "temperature": MODEL_TEMPERATURE = converted_value
                elif key == "max_tokens": MODEL_MAX_TOKENS = converted_value
                elif key == "top_p": MODEL_TOP_P = converted_value
                elif key == "frequency_penalty": MODEL_FREQUENCY_PENALTY = converted_value
                elif key == "presence_penalty": MODEL_PRESENCE_PENALTY = converted_value
                elif key == "reasoning_effort": MODEL_REASONING_EFFORT = converted_value
                elif key == "max_completion_tokens": MODEL_MAX_COMPLETION_TOKENS = converted_value
            except (ValueError, TypeError) as e:
                 print(f"Warning: Could not update parameter '{key}' with value '{value}'. Invalid type or value. Error: {e}", file=sys.stderr)
        else:
            # Parameter not relevant to the current model's config keys
             print(f"Warning: Parameter '{key}' not recognized or not applicable for model '{MODEL_CONFIG.get('model')}' (current params: {list(current_param_keys)}). Ignoring.", file=sys.stderr)

    # Update the deprecated global variables for potential backward compatibility
    MODEL_TEMPERATURE = MODEL_CONFIG.get("temperature")
    MODEL_MAX_TOKENS = MODEL_CONFIG.get("max_tokens")
    MODEL_TOP_P = MODEL_CONFIG.get("top_p")
    MODEL_FREQUENCY_PENALTY = MODEL_CONFIG.get("frequency_penalty")
    MODEL_PRESENCE_PENALTY = MODEL_CONFIG.get("presence_penalty")
    MODEL_REASONING_EFFORT = MODEL_CONFIG.get("reasoning_effort")
    MODEL_MAX_COMPLETION_TOKENS = MODEL_CONFIG.get("max_completion_tokens")

    if DEBUG:
        print(f"Model config updated. Current config: {get_model_config()}")

# --- Validation and Compatibility Notes ---
# 1. Ensure the actual OpenAI API names for 'o1', 'o3' etc. are used if they differ.
# 2. Code using the model should fetch config via `get_model_config()` and handle
#    potentially missing parameters (e.g., `config.get('top_p')` might be None).
# 3. Consider if `EVALUATOR_MODEL` needs its own parameter handling logic.
# 4. Verify the allowed values and type for `reasoning_effort` (string "low", "medium", "high").
# 5. Note the use of 'max_completion_tokens' for O-family models instead of 'max_tokens'. 