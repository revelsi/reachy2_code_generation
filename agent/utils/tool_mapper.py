#!/usr/bin/env python
"""
Tool mapper for the Reachy 2 robot.

This module provides functionality to discover and register tools for the Reachy 2 robot.
"""

import os
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Type, Callable, Optional, Union
import importlib.util
import pkgutil
from agent.tools.base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

# Configure path to include the agent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.dirname(current_dir)
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

# Output directories
SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "schemas")
os.makedirs(SCHEMAS_DIR, exist_ok=True)


class ReachyToolMapper:
    """
    A class that discovers and registers tools for the Reachy 2 robot.
    
    This class provides methods to discover tool classes, register tools from classes,
    and get tool schemas and implementations.
    """
    
    def __init__(self):
        """Initialize the tool mapper."""
        self.tool_schemas = {}
        self.tool_implementations = {}
        self.api_documentation = {}
    
    def discover_tool_classes(self, tools_package="agent.tools"):
        """
        Discover tool classes in the tools directory.
        
        Args:
            tools_package: The package path where tool classes are located.
            
        Returns:
            List[Type]: List of discovered tool classes.
        """
        discovered_classes = []
        
        # Import the tools package
        try:
            package = importlib.import_module(tools_package)
            package_path = os.path.dirname(package.__file__)
        except ImportError:
            print(f"Could not import tools package: {tools_package}")
            return discovered_classes
        
        # Walk through the package to find all modules
        for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
            if is_pkg:
                continue  # Skip subpackages
                
            # Import the module
            try:
                module = importlib.import_module(f"{tools_package}.{module_name}")
                
                # Find all classes in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, 'register_all_tools'):
                        discovered_classes.append(obj)
            except ImportError as e:
                print(f"Error importing module {module_name}: {e}")
        
        print(f"Discovered {len(discovered_classes)} tool classes")
        return discovered_classes
    
    def register_tools_from_classes(self, tool_classes=None):
        """
        Register tools from discovered classes.
        
        Args:
            tool_classes: Optional list of tool classes to register.
                If None, classes will be discovered automatically.
                
        Returns:
            int: Number of registered tools.
        """
        if tool_classes is None:
            tool_classes = self.discover_tool_classes()
        
        count = 0
        for cls in tool_classes:
            # Call the register_all_tools method to register tools
            if hasattr(cls, 'register_all_tools'):
                try:
                    # Register tools from the class
                    cls.register_all_tools()
                    
                    # Get the registered tools from the class
                    if hasattr(cls, 'tools') and hasattr(cls, 'tool_schemas'):
                        for name, schema in cls.tool_schemas.items():
                            implementation = cls.tools.get(name)
                            if implementation:
                                self.register_tool(name, schema, implementation)
                                count += 1
                except Exception as e:
                    print(f"Error registering tools from {cls.__name__}: {e}")
        
        print(f"Registered {count} tools from {len(tool_classes)} classes")
        return count
    
    def register_tool(self, name: str, schema: Dict[str, Any], implementation: Callable):
        """
        Register a tool with the given name, schema, and implementation.
        
        Args:
            name: The name of the tool.
            schema: The schema of the tool.
            implementation: The implementation of the tool.
            
        Raises:
            ValueError: If the schema is invalid.
        """
        # Validate schema
        if not isinstance(schema, dict):
            raise ValueError("Schema must be a dictionary")
        if not name:
            raise ValueError("Tool name is required")
        if not implementation:
            raise ValueError("Tool implementation is required")
        if not schema.get("description") and not (schema.get("function", {}).get("description")):
            raise ValueError("Tool description is required")
        if not schema.get("parameters") and not (schema.get("function", {}).get("parameters")):
            raise ValueError("Tool parameters are required")
            
        # Convert schema to LangChain/LangGraph format if needed
        if not self._is_langchain_format(schema):
            schema = self._convert_to_langchain_format(name, schema)
            
        self.tool_schemas[name] = schema
        self.tool_implementations[name] = implementation
    
    def _is_langchain_format(self, schema: Dict[str, Any]) -> bool:
        """
        Check if the schema is already in LangChain/LangGraph format.
        
        Args:
            schema: The schema to check.
            
        Returns:
            bool: True if the schema is in LangChain format, False otherwise.
        """
        # Check for LangChain tool format
        return (
            isinstance(schema, dict) and
            schema.get("type") == "function" and
            "function" in schema and
            "name" in schema.get("function", {}) and
            "description" in schema.get("function", {}) and
            "parameters" in schema.get("function", {})
        )
    
    def _convert_to_langchain_format(self, name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a schema to LangChain/LangGraph format.
        
        Args:
            name: The name of the tool.
            schema: The schema to convert.
            
        Returns:
            Dict[str, Any]: The converted schema.
        """
        # Extract description and parameters
        description = schema.get("description", "")
        parameters = schema.get("parameters", {})
        
        # Create LangChain tool format
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": schema.get("required", [])
                }
            }
        }
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Get the list of tool schemas.
        
        Returns:
            List[Dict[str, Any]]: List of tool schemas.
        """
        return list(self.tool_schemas.values())
    
    def get_tool_implementations(self) -> Dict[str, Callable]:
        """
        Get the dictionary of tool implementations.
        
        Returns:
            Dict[str, Callable]: Dictionary of tool implementations.
        """
        return self.tool_implementations
    
    def save_tool_definitions(self, output_path: str) -> bool:
        """
        Save tool definitions to a JSON file.
        
        Args:
            output_path: Path to save the tool definitions.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(self.tool_schemas, f, indent=2)
            print(f"Saved {len(self.tool_schemas)} tool definitions to {output_path}")
            return True
        except Exception as e:
            print(f"Error saving tool definitions: {e}")
            return False
    
    def load_api_documentation(self, doc_path=None) -> bool:
        """
        Load API documentation from a file or generate it.
        
        Args:
            doc_path: Optional path to the API documentation file.
                If None, documentation will be generated.
                
        Returns:
            bool: True if successful, False otherwise.
        """
        # If doc_path is provided, load from file
        if doc_path and os.path.exists(doc_path):
            try:
                with open(doc_path, 'r') as f:
                    sdk_docs = json.load(f)
                
                # Convert the list of documented items into a module-based dictionary
                self.api_documentation = {}
                for item in sdk_docs:
                    module_name = item.get("module", "")
                    if not module_name:
                        continue
                        
                    if module_name not in self.api_documentation:
                        self.api_documentation[module_name] = {
                            "functions": {},
                            "classes": {},
                            "docstring": ""
                        }
                    
                    # Process based on item type
                    if item["type"] == "module":
                        self.api_documentation[module_name]["docstring"] = item.get("docstring", "")
                        
                    elif item["type"] == "function":
                        self.api_documentation[module_name]["functions"][item["name"]] = {
                            "docstring": item.get("docstring", ""),
                            "parameters": item.get("parameters", {}),
                            "return_type": item.get("return_type"),
                            "source": item.get("source", ""),
                            "signature": item.get("signature", "")
                        }
                        
                    elif item["type"] == "class":
                        class_name = item["name"]
                        self.api_documentation[module_name]["classes"][class_name] = {
                            "docstring": item.get("docstring", ""),
                            "methods": {},
                            "bases": item.get("bases", [])
                        }
                        
                        # Process class methods
                        for method in item.get("methods", []):
                            method_name = method["name"]
                            self.api_documentation[module_name]["classes"][class_name]["methods"][method_name] = {
                                "docstring": method.get("docstring", ""),
                                "parameters": method.get("parameters", {}),
                                "return_type": method.get("return_type"),
                                "source": method.get("source", ""),
                                "signature": method.get("signature", ""),
                                "is_async": method.get("is_async", False),
                                "decorators": method.get("decorators", [])
                            }
                
                print(f"Loaded API documentation from {doc_path}")
                return True
            except Exception as e:
                print(f"Error loading API documentation: {e}")
                return False
        
        # Otherwise, try to generate documentation
        try:
            # Import the documentation generator
            from agent.utils.scrape_sdk_docs import extract_sdk_documentation
            
            # Extract documentation
            sdk_docs = extract_sdk_documentation()
            
            # Convert the list of documented items into a module-based dictionary
            self.api_documentation = {}
            for item in sdk_docs:
                module_name = item.get("module", "")
                if not module_name:
                    continue
                    
                if module_name not in self.api_documentation:
                    self.api_documentation[module_name] = {
                        "functions": {},
                        "classes": {},
                        "docstring": ""
                    }
                
                # Process based on item type
                if item["type"] == "module":
                    self.api_documentation[module_name]["docstring"] = item.get("docstring", "")
                    
                elif item["type"] == "function":
                    self.api_documentation[module_name]["functions"][item["name"]] = {
                        "docstring": item.get("docstring", ""),
                        "parameters": item.get("parameters", {}),
                        "return_type": item.get("return_type"),
                        "source": item.get("source", ""),
                        "signature": item.get("signature", "")
                    }
                    
                elif item["type"] == "class":
                    class_name = item["name"]
                    self.api_documentation[module_name]["classes"][class_name] = {
                        "docstring": item.get("docstring", ""),
                        "methods": {},
                        "bases": item.get("bases", [])
                    }
                    
                    # Process class methods
                    for method in item.get("methods", []):
                        method_name = method["name"]
                        self.api_documentation[module_name]["classes"][class_name]["methods"][method_name] = {
                            "docstring": method.get("docstring", ""),
                            "parameters": method.get("parameters", {}),
                            "return_type": method.get("return_type"),
                            "source": method.get("source", ""),
                            "signature": method.get("signature", ""),
                            "is_async": method.get("is_async", False),
                            "decorators": method.get("decorators", [])
                        }
            
            # Save the documentation if successful
            if self.api_documentation and doc_path:
                os.makedirs(os.path.dirname(doc_path), exist_ok=True)
                with open(doc_path, 'w') as f:
                    json.dump(sdk_docs, f, indent=2)
                print(f"Generated and saved API documentation to {doc_path}")
            return True
        except ImportError:
            print("Could not import SDK documentation generator. Running in demo/simulation mode.")
            return False
        except Exception as e:
            print(f"Error generating API documentation: {e}")
            return False
    
    def map_api_to_tools(self, focus_modules=None) -> Dict[str, Dict[str, Any]]:
        """
        Map API documentation to tool definitions.
        
        Args:
            focus_modules: Optional list of module names to focus on.
                
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of tool definitions.
        """
        if not self.api_documentation:
            print("No API documentation loaded. Call load_api_documentation first.")
            return {}
        
        tools = {}
        
        # Process each module in the API documentation
        for module_name, module_info in self.api_documentation.items():
            # Skip if not in focus_modules
            if focus_modules and not any(module_name.startswith(f"reachy2_sdk.{m}") for m in focus_modules):
                continue
            
            # Process standalone functions in the module
            for func_name, func_info in module_info.get("functions", {}).items():
                # Create a tool name
                tool_name = f"{module_name.replace('reachy2_sdk.', '').replace('.', '_')}_{func_name}"
                
                # Create tool schema
                description = func_info.get("docstring", "")
                parameters = {}
                required = []
                
                # Process parameters
                for param_name, param_type in func_info.get("parameters", {}).items():
                    if param_name == "self":
                        continue
                    
                    # Map Python types to JSON Schema types
                    json_type = self._map_python_type_to_json_schema(param_type)
                    
                    # Extract parameter description from docstring if available
                    param_desc = f"Parameter {param_name}"
                    if description:
                        # Look for parameter description in docstring
                        param_lines = [line.strip() for line in description.split("\n") if line.strip().startswith(f"{param_name}:")]
                        if param_lines:
                            param_desc = param_lines[0].split(":", 1)[1].strip()
                    
                    parameters[param_name] = {
                        "type": json_type,
                        "description": param_desc
                    }
                    
                    # Add to required if no default value is indicated in signature
                    if "=" not in func_info.get("signature", "").split(param_name)[1].split(",")[0]:
                        required.append(param_name)
                
                # Create the tool schema
                tools[tool_name] = {
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": parameters,
                            "required": required
                        }
                    },
                    "module": module_name,
                    "source": func_info.get("source", ""),
                    "return_type": func_info.get("return_type")
                }
            
            # Process classes in the module
            for class_name, class_info in module_info.get("classes", {}).items():
                # Process class methods
                for method_name, method_info in class_info.get("methods", {}).items():
                    # Skip private methods and special methods unless they're properties
                    if (method_name.startswith("_") and 
                        not method_name.startswith("__") and 
                        "property" not in method_info.get("decorators", [])):
                        continue
                    
                    # Create a tool name
                    tool_name = f"{module_name.replace('reachy2_sdk.', '').replace('.', '_')}_{class_name}_{method_name}"
                    
                    # Create tool schema
                    description = method_info.get("docstring", "")
                    if not description and class_info.get("docstring"):
                        description = f"Method of {class_name}: {class_info['docstring']}"
                    
                    parameters = {}
                    required = []
                    
                    # Process parameters
                    for param_name, param_type in method_info.get("parameters", {}).items():
                        if param_name == "self":
                            continue
                        
                        # Map Python types to JSON Schema types
                        json_type = self._map_python_type_to_json_schema(param_type)
                        
                        # Extract parameter description from docstring if available
                        param_desc = f"Parameter {param_name}"
                        if description:
                            # Look for parameter description in docstring
                            param_lines = [line.strip() for line in description.split("\n") if line.strip().startswith(f"{param_name}:")]
                            if param_lines:
                                param_desc = param_lines[0].split(":", 1)[1].strip()
                        
                        parameters[param_name] = {
                            "type": json_type,
                            "description": param_desc
                        }
                        
                        # Add to required if no default value is indicated in signature
                        if "=" not in method_info.get("signature", "").split(param_name)[1].split(",")[0]:
                            required.append(param_name)
                    
                    # Create the tool schema
                    tools[tool_name] = {
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "description": description,
                            "parameters": {
                                "type": "object",
                                "properties": parameters,
                                "required": required
                            }
                        },
                        "module": module_name,
                        "class": class_name,
                        "source": method_info.get("source", ""),
                        "return_type": method_info.get("return_type"),
                        "is_async": method_info.get("is_async", False),
                        "is_property": "property" in method_info.get("decorators", [])
                    }
        
        return tools
    
    def _map_python_type_to_json_schema(self, python_type: str) -> str:
        """
        Map Python type to JSON Schema type.
        
        Args:
            python_type: Python type as string.
            
        Returns:
            str: Corresponding JSON Schema type.
        """
        type_mapping = {
            "int": "integer",
            "float": "number",
            "str": "string",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
            "None": "null",
        }
        
        # Handle common type patterns
        if python_type.startswith("List[") or python_type.startswith("list["):
            return "array"
        elif python_type.startswith("Dict[") or python_type.startswith("dict["):
            return "object"
        elif python_type.startswith("Union[") or python_type.startswith("Optional["):
            # For union types, use the first non-None type
            inner_types = python_type.split("[", 1)[1].rsplit("]", 1)[0].split(",")
            for inner_type in inner_types:
                inner_type = inner_type.strip()
                if inner_type != "None":
                    return self._map_python_type_to_json_schema(inner_type)
            return "string"  # Default to string if can't determine
        
        # Use the mapping or default to string
        return type_mapping.get(python_type, "string")
    
    def generate_tool_implementations(self, output_dir: str) -> bool:
        """
        Generate tool implementation files.
        
        Args:
            output_dir: Directory to save the implementation files.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.tool_schemas:
            print("No tool schemas loaded. Call map_api_to_tools first.")
            return False
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Group tools by module
        tools_by_module = {}
        for tool_name, tool_info in self.tool_schemas.items():
            module = tool_info.get("module", "").replace("reachy2_sdk.", "")
            module = module.split(".")[0] if module else "misc"
            
            if module not in tools_by_module:
                tools_by_module[module] = []
            
            tool_info['name'] = tool_name
            tools_by_module[module].append(tool_info)

        # Template for the tool implementation file
        TOOL_FILE_TEMPLATE = '''#!/usr/bin/env python
"""
{module_name} tools for the Reachy 2 robot.

This module provides tools for interacting with the {module_name} module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class {class_name}(BaseTool):
    """Tools for interacting with the {module_name} module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all {module_name} tools."""
{tool_registrations}
'''

        # Template for each tool implementation
        TOOL_IMPL_TEMPLATE = '''
    @classmethod
    def {func_name}(cls, {params}) -> Dict[str, Any]:
        """{docstring}"""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            {target_obj_code}

            # Call the function with parameters
            result = {call_code}

            return {{
                "success": True,
                "result": result
            }}
        except Exception as e:
            return {{
                "success": False,
                "error": str(e)
            }}
'''

        try:
            # Generate implementation files for each module
            for module_name, tools in tools_by_module.items():
                class_name = f"{module_name.title().replace('_', '')}Tools"
                tool_impls = []
                tool_registrations = []

                for tool in tools:
                    # Extract tool information
                    name = tool['name']
                    description = tool.get('function', {}).get('description', '') or tool.get('description', '')
                    parameters = tool.get('function', {}).get('parameters', {}).get('properties', {}) or tool.get('parameters', {}).get('properties', {})
                    required = tool.get('function', {}).get('parameters', {}).get('required', []) or tool.get('parameters', {}).get('required', [])

                    # Generate parameter string
                    param_list = []
                    for param_name in parameters:
                        if param_name == 'cls':  # Skip cls parameter as it's already included
                            continue
                        if param_name in required:
                            param_list.append(param_name)
                        else:
                            param_list.append(f"{param_name}=None")
                    params = ", ".join(param_list)

                    # Parse the function name to determine the proper object and call
                    parts = name.split('_')
                    if len(parts) >= 3:
                        module = parts[0]
                        class_name_part = parts[1]
                        method_name = '_'.join(parts[2:])
                        
                        # Handle different types of calls
                        if class_name_part.lower() == module.lower():
                            # Module-level function
                            target_obj_code = f"obj = reachy.{module}"
                            call_code = f"obj.{method_name}({', '.join(param_list)})"
                        else:
                            # Class method
                            target_obj_code = f"obj = getattr(reachy, '{class_name_part.lower()}')"
                            call_code = f"obj.{method_name}({', '.join(param_list)})"
                    else:
                        # Direct module function
                        target_obj_code = "obj = reachy"
                        call_code = f"obj.{name}({', '.join(param_list)})"

                    # Format docstring
                    docstring = description.replace('\n', '\n        ')

                    # Generate tool implementation
                    impl = TOOL_IMPL_TEMPLATE.format(
                        func_name=name,
                        params=params,
                        docstring=docstring,
                        target_obj_code=target_obj_code,
                        call_code=call_code
                    )
                    tool_impls.append(impl)

                    # Generate tool registration
                    registration = f'''        cls.register_tool(
            name="{name}",
            func=cls.{name},
            schema=cls.create_tool_schema(
                name="{name}",
                description="""{description}""",
                parameters={parameters},
                required={required}
            )
        )'''
                    tool_registrations.append(registration)

                # Combine all implementations
                file_content = TOOL_FILE_TEMPLATE.format(
                    module_name=module_name,
                    class_name=class_name,
                    tool_registrations='\n'.join(tool_registrations)
                ) + '\n'.join(tool_impls)

                # Write the implementation file
                output_path = os.path.join(output_dir, f"{module_name}_tools.py")
                with open(output_path, 'w') as f:
                    f.write(file_content)

            return True
        except Exception as e:
            print(f"Error generating implementations: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    mapper = ReachyToolMapper()
    mapper.discover_tool_classes()
    mapper.register_tools_from_classes()
    mapper.save_tool_definitions(os.path.join(SCHEMAS_DIR, "reachy_tools.json")) 