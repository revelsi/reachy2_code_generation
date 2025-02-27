#!/usr/bin/env python
"""Pytest configuration file."""

import os
import sys
import pytest

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ["REACHY_TESTING"] = "1"
    yield
    os.environ.pop("REACHY_TESTING", None) 