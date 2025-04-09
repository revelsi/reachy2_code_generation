#!/usr/bin/env python
import ast
import importlib
import inspect
import json
import os
import pkgutil
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, get_type_hints
import re

import nbformat

# Repository and directory configuration
REACHY_SDK_GIT_URL = "https://github.com/pollen-robotics/reachy2-sdk.git"
POLLEN_VISION_GIT_URL = "https://github.com/pollen-robotics/pollen-vision.git"

# Output directories - adjust paths for new location
RAW_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data/raw_docs")
EXTRACTED_DIR = os.path.join(RAW_DOCS_DIR, "extracted")
EXTERNAL_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data/external_docs/documents")
os.makedirs(EXTRACTED_DIR, exist_ok=True)
os.makedirs(EXTERNAL_DOCS_DIR, exist_ok=True)

# Repository directories
REPO_DIR = os.path.join(RAW_DOCS_DIR, "reachy2_sdk_repo")
SDK_SOURCE_DIR = os.path.join(REPO_DIR, "src", "reachy2_sdk")
EXAMPLES_SOURCE_DIR = os.path.join(REPO_DIR, "src", "examples")
TUTORIALS_SOURCE_DIR = os.path.join(RAW_DOCS_DIR, "reachy2_tutorials")

# Vision repository directories
VISION_REPO_DIR = os.path.join(RAW_DOCS_DIR, "pollen_vision_repo")
VISION_SOURCE_DIR = os.path.join(VISION_REPO_DIR, "src", "pollen_vision")

# Legacy directories (kept for compatibility)
API_DOCS_DIR = os.path.join(RAW_DOCS_DIR, "api_docs")
EXAMPLES_DIR = os.path.join(RAW_DOCS_DIR, "examples")
TUTORIALS_DIR = os.path.join(RAW_DOCS_DIR, "tutorials")


def is_valid_git_repo(repo_path):
    """Check if the directory is a valid Git repository."""
    try:
        # Check if .git directory exists
        git_dir = os.path.join(repo_path, ".git")
        if not os.path.exists(git_dir) or not os.path.isdir(git_dir):
            return False
        
        # Try running a git command to verify it's a valid repo
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def clone_or_update_repo(repo_url, repo_dir, force_clone=False):
    """
    Clone the repository if it doesn't exist, or pull the latest changes.
    
    Args:
        repo_url: The Git URL of the repository to clone.
        repo_dir: The directory to clone the repository into.
        force_clone: If True, delete the existing repository and clone it again.
                    Useful for handling corrupted repositories.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # If force_clone is True, remove the existing repository
        if force_clone and os.path.exists(repo_dir):
            print(f"Force clone requested. Removing existing repository at {repo_dir}...")
            shutil.rmtree(repo_dir, ignore_errors=True)
        
        # Check if the repository exists and is valid
        if os.path.exists(repo_dir):
            if is_valid_git_repo(repo_dir):
                print("Repository exists. Pulling latest changes...")
                result = subprocess.run(
                    ["git", "-C", repo_dir, "pull"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Repository updated successfully: {result.stdout.strip()}")
            else:
                print(f"Directory exists but is not a valid Git repository: {repo_dir}")
                print("Removing invalid repository and cloning again...")
                shutil.rmtree(repo_dir, ignore_errors=True)
                print(f"Cloning repository: {repo_url} into {repo_dir}...")
                result = subprocess.run(
                    ["git", "clone", repo_url, repo_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Repository cloned successfully: {result.stdout.strip()}")
        else:
            print(f"Cloning repository: {repo_url} into {repo_dir}...")
            os.makedirs(os.path.dirname(repo_dir), exist_ok=True)
            result = subprocess.run(
                ["git", "clone", repo_url, repo_dir],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"Repository cloned successfully: {result.stdout.strip()}")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")
        print(f"Command output: {e.stdout if hasattr(e, 'stdout') else 'No output'}")
        print(f"Command error: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
        
        # Try to recover by forcing a clone on the next run
        print("Suggesting to use force_clone=True on the next run to recover.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def process_python_file(file_path: str, repo_base_dir: str, collection_name: str = "reachy2_sdk") -> Dict:
    """Process a Python file into a document."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse the file to get docstring and other metadata
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree) or ""

        # Get relative path for source tracking
        rel_path = os.path.relpath(file_path, repo_base_dir)

        return {
            "content": content,
            "metadata": {
                "source": rel_path,
                "type": "example",
                "format": "python",
                "collection": collection_name,
                "docstring": docstring,
            },
        }
    except Exception as e:
        print(f"Error processing Python file {file_path}: {e}")
        return None


def process_notebook_file(file_path: str, repo_base_dir: str, collection_name: str = "reachy2_sdk") -> Dict:
    """Process a Jupyter notebook into a document."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        # Extract markdown and code cells
        content = []
        for cell in nb.cells:
            if cell.cell_type == "markdown":
                content.append(f"# {cell.source}")
            elif cell.cell_type == "code":
                content.append(f"```python\n{cell.source}\n```")

        # Get relative path for source tracking
        rel_path = os.path.relpath(file_path, repo_base_dir)

        # Get notebook title from filename
        title = os.path.splitext(os.path.basename(file_path))[0]

        return {
            "content": "\n\n".join(content),
            "metadata": {
                "source": rel_path,
                "type": "example",
                "format": "notebook",
                "collection": collection_name,
                "title": title,
            },
        }
    except Exception as e:
        print(f"Error processing notebook {file_path}: {e}")
        return None


def collect_sdk_examples() -> List[Dict]:
    """Collect examples from the SDK repository."""
    print("\nCollecting SDK examples...")
    examples = []

    if not os.path.exists(EXAMPLES_SOURCE_DIR):
        print(f"Warning: Examples directory not found at {EXAMPLES_SOURCE_DIR}")
        return examples

    # Walk through the examples directory
    for root, _, files in os.walk(EXAMPLES_SOURCE_DIR):
        for file in sorted(files):  # Sort files to process in a consistent order
            if not (file.endswith(".py") or file.endswith(".ipynb")):
                continue

            file_path = os.path.join(root, file)
            print(f"Processing: {file}")

            if file.endswith(".py"):
                doc = process_python_file(file_path, REPO_DIR, "reachy2_sdk")
                if doc:
                    examples.append(doc)
                    print(f"Added Python example: {file}")

            elif file.endswith(".ipynb"):
                doc = process_notebook_file(file_path, REPO_DIR, "reachy2_sdk")
                if doc:
                    examples.append(doc)
                    print(f"Added notebook example: {file}")

    print(f"Collected {len(examples)} examples")
    return examples


def get_function_signature(node: ast.FunctionDef) -> str:
    """Extract function signature from AST node."""
    args = []

    # Add positional args
    for arg in node.args.args:
        arg_str = arg.arg
        if arg.annotation:
            arg_str += f": {ast.unparse(arg.annotation)}"
        args.append(arg_str)

    # Add vararg if present
    if node.args.vararg:
        args.append(f"*{node.args.vararg.arg}")

    # Add keyword args
    for arg in node.args.kwonlyargs:
        arg_str = arg.arg
        if arg.annotation:
            arg_str += f": {ast.unparse(arg.annotation)}"
        args.append(arg_str)

    # Add kwargs if present
    if node.args.kwarg:
        args.append(f"**{node.args.kwarg.arg}")

    # Add return annotation if present
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""

    return f"({', '.join(args)}){returns}"


def get_return_annotation(node: ast.FunctionDef) -> Optional[str]:
    """Extract return type annotation from AST node."""
    if node.returns:
        return ast.unparse(node.returns)
    return None


def get_parameters(node: ast.FunctionDef) -> Dict[str, str]:
    """Extract parameter annotations from AST node."""
    params = {}
    for arg in node.args.args:
        if arg.annotation:
            params[arg.arg] = ast.unparse(arg.annotation)
        else:
            params[arg.arg] = "Any"
    return params


def process_function_def(node: ast.FunctionDef, module_name: str, parent_class: str = None, source=None) -> Dict:
    """
    Process a function definition node.
    
    Args:
        node: The AST function definition node
        module_name: The module name
        parent_class: The parent class name, if this is a method
        source: The source code, if available
        
    Returns:
        Dict: A dictionary with function/method information
    """
    # Include more functions, but still skip private ones (single underscore)
    # Include special methods (double underscore) and property methods
    if (
        not node.name.startswith("_") 
        or node.name.startswith("__") 
        or any(
            isinstance(d, ast.Name) and d.id == "property"
            for d in node.decorator_list
        )
    ):
        # Get docstring and clean it
        docstring = ast.get_docstring(node) or ""
        
        # Extract decorators as list of strings
        decorators = []
        for d in node.decorator_list:
            if isinstance(d, ast.Name):
                decorators.append(d.id)
            elif isinstance(d, ast.Call) and isinstance(d.func, ast.Name):
                decorators.append(d.func.id)
            elif isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute):
                decorators.append(f"{d.func.value.id}.{d.func.attr}")
            elif isinstance(d, ast.Attribute):
                decorators.append(f"{d.value.id}.{d.attr}")
        
        return {
            "type": "function" if not parent_class else "method",
            "name": node.name,
            "module": module_name,
            "class": parent_class,  # Will be None for standalone functions
            "signature": get_function_signature(node),
            "docstring": inspect.cleandoc(docstring),
            "return_type": get_return_annotation(node),
            "parameters": get_parameters(node),
            "source": f"{module_name}.{parent_class + '.' if parent_class else ''}{node.name}",
            "decorators": decorators,
        }
    return None


def extract_code_from_directory(directory_path: str, collection_name: str) -> List[Dict]:
    """
    Extract API documentation from Python files in a directory.
    
    Args:
        directory_path: The directory to process.
        collection_name: The name of the collection (e.g., "reachy2_sdk" or "pollen_vision").
        
    Returns:
        List[Dict]: A list of API documentation items.
    """
    documented_items = []
    
    if not os.path.exists(directory_path):
        print(f"Warning: Source directory not found at {directory_path}")
        return documented_items

    # Walk through each Python file in the source directory
    for root, _, files in os.walk(directory_path):
        for file in sorted(files):
            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)
            
            # Determine the module name from the file path
            module_rel_path = os.path.relpath(file_path, directory_path)
            module_name = module_rel_path.replace("/", ".").replace("\\", ".")
            if module_name.endswith(".py"):
                module_name = module_name[:-3]  # Remove .py extension
            
            # Use the appropriate module prefix
            if collection_name == "reachy2_sdk":
                full_module_name = f"reachy2_sdk.{module_name}"
            elif collection_name == "pollen_vision":
                # For pollen_vision, handle any special cases
                full_module_name = f"pollen_vision.{module_name}"
                # Remove src prefix if present
                if full_module_name.startswith("pollen_vision.src."):
                    full_module_name = full_module_name.replace("pollen_vision.src.", "pollen_vision.")
            else:
                full_module_name = module_name

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()

                # Parse the file using AST
                tree = ast.parse(source)
                module_docstring = ast.get_docstring(tree) or ""

                # Add module documentation
                documented_items.append({
                    "type": "module",
                    "name": full_module_name,
                    "docstring": module_docstring
                })
                
                # Keep track of classes for later class method processing
                classes = {}

                # First pass: collect classes and functions
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.ClassDef):
                        class_doc = {
                            "type": "class",
                            "name": node.name,
                            "module": full_module_name,
                            "docstring": ast.get_docstring(node) or "",
                            "methods": [],
                            "bases": [
                                base.id if isinstance(base, ast.Name) else 
                                (f"{base.value.id}.{base.attr}" if isinstance(base, ast.Attribute) else "object")
                                for base in node.bases
                                if isinstance(base, (ast.Name, ast.Attribute))
                            ]
                        }
                        
                        # Store class for later method processing
                        classes[node.name] = class_doc
                        
                        # Process methods directly in the class body
                        for class_item in node.body:
                            if isinstance(class_item, ast.FunctionDef):
                                method_doc = process_function_def(
                                    class_item, 
                                    full_module_name, 
                                    node.name, 
                                    source
                                )
                                if method_doc:
                                    class_doc["methods"].append(method_doc)
                        
                        documented_items.append(class_doc)
                    
                    elif isinstance(node, ast.FunctionDef):
                        # Process top-level functions
                        func_doc = process_function_def(
                            node, 
                            full_module_name, 
                            None, 
                            source
                        )
                        if func_doc:
                            documented_items.append(func_doc)

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                import traceback
                traceback.print_exc()

    return documented_items


def extract_sdk_documentation() -> List[Dict]:
    """Extract API documentation directly from SDK Python source files."""
    print("\nExtracting SDK API documentation...")
    
    # Extract documentation from the Reachy 2 SDK
    reachy_sdk_docs = extract_code_from_directory(SDK_SOURCE_DIR, "reachy2_sdk")
    print(f"Extracted {len(reachy_sdk_docs)} documentation items from Reachy 2 SDK")
    
    return reachy_sdk_docs


def should_extract_vision_documentation() -> bool:
    """
    Determine if vision documentation should be extracted.
    
    This checks environment variables and/or whether pollen_vision is installed.
    
    Returns:
        bool: True if vision documentation should be extracted, False otherwise.
    """
    # Check environment variable
    if os.environ.get("EXTRACT_VISION_DOCS", "").lower() in ("1", "true", "yes"):
        return True
        
    # Check if pollen_vision is installed
    try:
        import importlib.util
        if importlib.util.find_spec("pollen_vision") is not None:
            return True
    except ImportError:
        pass
        
    return False


def extract_vision_documentation() -> List[Dict]:
    """Extract API documentation from the pollen-vision repository."""
    print("\nExtracting pollen-vision API documentation...")
    
    # Extract documentation from the pollen-vision repository
    vision_docs = extract_code_from_directory(VISION_SOURCE_DIR, "pollen_vision")
    print(f"Extracted {len(vision_docs)} documentation items from pollen-vision")
    
    return vision_docs


def save_sdk_documentation(sdk_docs: List[Dict], examples: List[Dict], vision_docs: List[Dict] = None):
    """
    Save raw SDK documentation and examples to appropriate files.
    
    This function only saves the raw documentation. The processing and optimization
    of documentation for code generation is handled by tool_mapper.py.
    """
    print("\nSaving raw documentation...")

    # Save raw SDK API documentation
    api_docs_path = os.path.join(EXTRACTED_DIR, "raw_api_docs.json")
    
    # Combine SDK and vision docs if vision docs are available
    all_docs = sdk_docs.copy()
    if vision_docs:
        all_docs.extend(vision_docs)
        print(f"Combined {len(sdk_docs)} SDK docs with {len(vision_docs)} vision docs")
    
    with open(api_docs_path, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2)
    print(f"Saved {len(all_docs)} API documentation items to {api_docs_path}")

    # Save examples
    examples_path = os.path.join(EXTRACTED_DIR, "raw_sdk_examples.json")
    with open(examples_path, "w", encoding="utf-8") as f:
        json.dump(examples, f, indent=2)
    print(f"Saved {len(examples)} examples to {examples_path}")
    
    # Create agent docs directory for future use by tool_mapper.py
    agent_docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    os.makedirs(agent_docs_dir, exist_ok=True)
    print(f"Prepared agent docs directory at {agent_docs_dir}")
    print("Note: The optimized api_documentation.json will be created by tool_mapper.py")


def main():
    """Main function to scrape SDK documentation and examples."""
    print("Starting SDK documentation scraping...")

    # Step 1: Clone/update the repositories
    # Always clone/update the Reachy 2 SDK repository
    if not clone_or_update_repo(REACHY_SDK_GIT_URL, REPO_DIR):
        print("Failed to clone/update Reachy 2 SDK repository. Trying with force_clone=True...")
        if not clone_or_update_repo(REACHY_SDK_GIT_URL, REPO_DIR, force_clone=True):
            print("Failed to clone Reachy 2 SDK repository even with force_clone=True. Aborting.")
            return
    
    # Check if we should extract vision documentation
    extract_vision = should_extract_vision_documentation()
    vision_docs = None
    
    if extract_vision:
        print("Vision documentation extraction requested.")
        # Clone/update the pollen-vision repository
        if not clone_or_update_repo(POLLEN_VISION_GIT_URL, VISION_REPO_DIR):
            print("Failed to clone/update pollen-vision repository. Trying with force_clone=True...")
            if not clone_or_update_repo(POLLEN_VISION_GIT_URL, VISION_REPO_DIR, force_clone=True):
                print("Failed to clone pollen-vision repository even with force_clone=True.")
                print("Will continue without vision documentation.")
                extract_vision = False
    else:
        print("Vision documentation extraction not requested. Skipping.")

    # Step 2: Extract SDK API documentation
    sdk_docs = extract_sdk_documentation()
    print(f"Extracted documentation for {len(sdk_docs)} items from Reachy 2 SDK")
    
    # Step 3: Extract vision API documentation if requested
    if extract_vision:
        vision_docs = extract_vision_documentation()
        print(f"Extracted documentation for {len(vision_docs)} items from pollen-vision")

    # Step 4: Collect SDK examples
    examples = collect_sdk_examples()
    print(f"Collected {len(examples)} examples")

    # Step 5: Save documentation and examples
    save_sdk_documentation(sdk_docs, examples, vision_docs)

    print("\nSDK documentation scraping complete!")


if __name__ == "__main__":
    main()
