#!/usr/bin/env python
"""
Test script to verify that all dependencies are working correctly together.
"""

import os
import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report success/failure."""
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"✅ Successfully imported {module_name}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        print(f"   Try reinstalling with: pip install {package_name}")
        return False

def main():
    """Main function to test dependencies."""
    print(f"Python version: {sys.version}")
    print("Testing imports...\n")
    
    # Core dependencies
    imports = [
        ("openai", "openai"),
        ("dotenv", "python-dotenv"),
        ("flask", "flask"),
        ("flask_cors", "flask-cors"),
        ("websockets", "websockets"),
        ("psutil", "psutil"),
        
        # LangChain ecosystem
        ("langchain", "langchain"),
        ("langgraph", "langgraph"),
        ("langchain_openai", "langchain-openai"),
        ("pydantic", "pydantic"),
        
        # Optional dependencies
        ("gradio", "gradio"),
        
        # Visualization and data processing
        ("matplotlib", "matplotlib"),
        ("networkx", "networkx"),
        ("numpy", "numpy"),
        ("pyquaternion", "pyquaternion"),
    ]
    
    # Try to import each module
    failures = 0
    for module_name, package_name in imports:
        if not check_import(module_name, package_name):
            failures += 1
    
    # Try to import and use LangChain components
    try:
        from langchain.schema import Document
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
        from langgraph.graph import StateGraph
        
        print("\n✅ Successfully imported and initialized LangChain components")
    except Exception as e:
        print(f"\n❌ Failed to initialize LangChain components: {e}")
        failures += 1
    
    # Summary
    print("\nTest Summary:")
    if failures == 0:
        print("✅ All dependencies are working correctly!")
    else:
        print(f"❌ {failures} dependencies failed to import correctly.")
    
    return failures

if __name__ == "__main__":
    sys.exit(main()) 