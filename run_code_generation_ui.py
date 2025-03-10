#!/usr/bin/env python
"""
Run script for the Reachy 2 Code Generation Interface.

This script provides a simple way to launch the code generation interface.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the current directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the code generation interface
from agent.code_generation_interface import main

if __name__ == "__main__":
    # Run the code generation interface with command line arguments
    main() 