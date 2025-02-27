#!/usr/bin/env python
"""Unit tests for Reachy tools."""

import os
import json
import pytest
from typing import Dict, Any, List
from langchain.tools import BaseTool
from langchain.schema import FunctionMessage

from agent.utils.tool_mapper import ReachyToolMapper
from agent.tools.base_tool import BaseTool as ReachyBaseTool

class TestReachyTools:
    """Test suite for Reachy tools."""
    
    @pytest.fixture
    def tool_mapper(self) -> ReachyToolMapper:
        """Fixture to provide a tool mapper instance."""
        mapper = ReachyToolMapper()
        # Load API documentation from the test data
        doc_path = os.path.join("agent", "docs", "api_documentation.json")
        assert mapper.load_api_documentation(doc_path)
        return mapper
    
    @pytest.fixture
    def tool_schemas(self, tool_mapper) -> Dict[str, Dict[str, Any]]:
        """Fixture to provide tool schemas."""
        tools = tool_mapper.map_api_to_tools()
        assert tools, "No tools were generated"
        return tools
    
    def test_tool_schema_format(self, tool_schemas):
        """Test that all tool schemas follow the LangChain format."""
        for name, schema in tool_schemas.items():
            # Check basic structure
            assert "type" in schema
            assert schema["type"] == "function"
            assert "function" in schema
            
            # Check function schema
            func_schema = schema["function"]
            assert "name" in func_schema
            assert "description" in func_schema
            assert "parameters" in func_schema
            
            # Check parameters schema
            params = func_schema["parameters"]
            assert "type" in params
            assert params["type"] == "object"
            assert "properties" in params
            
            # If required parameters are specified, they should exist in properties
            if "required" in params:
                for req_param in params["required"]:
                    assert req_param in params["properties"]
    
    def test_tool_implementation_generation(self, tool_mapper, tmp_path):
        """Test that tool implementations are generated correctly."""
        # Generate implementations in a temporary directory
        output_dir = str(tmp_path)
        
        # Set tool schemas
        tool_mapper.tool_schemas = tool_mapper.map_api_to_tools()
        assert tool_mapper.tool_schemas, "No tool schemas were generated"
        
        # Generate implementations
        assert tool_mapper.generate_tool_implementations(output_dir)
        
        # Check that files were generated
        files = os.listdir(output_dir)
        assert files, "No implementation files were generated"
        
        # Check each implementation file
        for file in files:
            if not file.endswith("_tools.py"):
                continue
                
            file_path = os.path.join(output_dir, file)
            with open(file_path, "r") as f:
                content = f.read()
                
            # Check basic structure
            assert "class" in content
            assert "BaseTool" in content
            assert "register_all_tools" in content
            assert "get_reachy_connection" in content
    
    def test_tool_registration(self, tool_mapper, tool_schemas):
        """Test that tools can be registered and accessed."""
        # Register tools
        tool_mapper.tool_schemas = tool_schemas
        assert tool_mapper.get_tool_schemas()
        
        # Check that we can get implementations
        impls = tool_mapper.get_tool_implementations()
        assert isinstance(impls, dict)
    
    def test_tool_error_handling(self, tool_mapper, tmp_path):
        """Test that tools handle errors appropriately."""
        # Generate implementations
        output_dir = str(tmp_path)
        
        # Set tool schemas
        tool_mapper.tool_schemas = tool_mapper.map_api_to_tools()
        assert tool_mapper.tool_schemas, "No tool schemas were generated"
        
        # Generate implementations
        assert tool_mapper.generate_tool_implementations(output_dir)
        
        # Check error handling in generated code
        files = os.listdir(output_dir)
        for file in files:
            if not file.endswith("_tools.py"):
                continue
                
            file_path = os.path.join(output_dir, file)
            with open(file_path, "r") as f:
                content = f.read()
                
            # Verify error handling structure
            assert "try:" in content
            assert "except Exception as e:" in content
            assert '"success": False' in content
            assert '"error": str(e)' in content
    
    def test_tool_docstrings(self, tool_schemas):
        """Test that tools have proper docstrings."""
        for name, schema in tool_schemas.items():
            description = schema["function"]["description"]
            assert description, f"Tool {name} is missing a description"
            assert len(description.strip()) > 0
    
    def test_tool_parameter_types(self, tool_schemas):
        """Test that tool parameters have valid types."""
        valid_types = {"string", "number", "integer", "boolean", "array", "object", "null"}
        
        for name, schema in tool_schemas.items():
            properties = schema["function"]["parameters"]["properties"]
            for param_name, param_info in properties.items():
                assert "type" in param_info
                assert param_info["type"] in valid_types
    
    def test_tool_required_parameters(self, tool_schemas):
        """Test that required parameters are properly specified."""
        for name, schema in tool_schemas.items():
            params = schema["function"]["parameters"]
            if "required" in params:
                required = params["required"]
                properties = params["properties"]
                
                # All required parameters should exist in properties
                for req_param in required:
                    assert req_param in properties
                    
                # Required parameters should have descriptions
                for req_param in required:
                    assert "description" in properties[req_param]
    
    def test_tool_return_format(self, tool_mapper, tmp_path):
        """Test that tools return results in the correct format."""
        # Generate implementations
        output_dir = str(tmp_path)
        
        # Set tool schemas
        tool_mapper.tool_schemas = tool_mapper.map_api_to_tools()
        assert tool_mapper.tool_schemas, "No tool schemas were generated"
        
        # Generate implementations
        assert tool_mapper.generate_tool_implementations(output_dir)
        
        # Check return format in generated code
        files = os.listdir(output_dir)
        for file in files:
            if not file.endswith("_tools.py"):
                continue
                
            file_path = os.path.join(output_dir, file)
            with open(file_path, "r") as f:
                content = f.read()
                
            # Verify return format
            assert 'return {' in content
            assert '"success": True' in content
            assert '"result": result' in content
            assert '"success": False' in content
            assert '"error": str(e)' in content 