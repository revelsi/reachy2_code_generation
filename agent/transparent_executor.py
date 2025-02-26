#!/usr/bin/env python
"""
Transparent function executor for Reachy agent.

This module provides a transparent execution framework that shows reasoning,
function calls, and requests permission before executing actions on the robot.
"""

import inspect
import json
import logging
import time
from typing import Any, Dict, List, Callable, Optional, Union, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("transparent_executor")

class TransparentExecutor:
    """
    Transparent executor that shows reasoning and function calls.
    
    This class wraps tool functions to provide a transparent execution flow that:
    1. Shows the reasoning behind each function call
    2. Displays the function call with parameters
    3. Requests user permission before execution
    4. Shows execution results
    """
    
    def __init__(
        self, 
        auto_approve: bool = False,
        dry_run: bool = False,
        use_mock: bool = False,
        verbose: bool = True
    ):
        """
        Initialize the transparent executor.
        
        Args:
            auto_approve: Whether to automatically approve function calls without user confirmation
            dry_run: Whether to skip actual execution and just simulate results
            use_mock: Whether to use mock implementations when available
            verbose: Whether to print detailed information
        """
        self.auto_approve = auto_approve
        self.dry_run = dry_run
        self.use_mock = use_mock
        self.verbose = verbose
        self.execution_history = []
        self._function_registry = {}
        
    def register_function(self, func: Callable, mock_func: Optional[Callable] = None) -> Callable:
        """
        Register a function with the executor.
        
        Args:
            func: Function to register
            mock_func: Optional mock implementation of the function
            
        Returns:
            Callable: Wrapped function that goes through the transparent execution flow
        """
        function_name = func.__name__
        
        # Store the original function and mock implementation
        self._function_registry[function_name] = {
            "func": func,
            "mock_func": mock_func,
            "signature": inspect.signature(func),
            "doc": func.__doc__
        }
        
        # Create a wrapped function
        def wrapped_function(*args, **kwargs):
            return self.execute_function(function_name, *args, **kwargs)
        
        # Copy metadata from original function
        wrapped_function.__name__ = function_name
        wrapped_function.__doc__ = func.__doc__
        wrapped_function.__signature__ = inspect.signature(func)
        
        return wrapped_function
    
    def execute_function(
        self, 
        function_name: str,
        reasoning: Optional[str] = None,
        *args, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a function with transparent steps.
        
        Args:
            function_name: Name of the function to execute
            reasoning: Reasoning behind this function call
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Dict[str, Any]: Execution result
        """
        # Get function info
        func_info = self._function_registry.get(function_name)
        if not func_info:
            return {
                "success": False,
                "error": f"Function {function_name} not registered"
            }
        
        # Format parameters for display
        parameters = self._format_parameters(func_info, *args, **kwargs)
        
        # Record execution info
        execution_info = {
            "timestamp": time.time(),
            "function": function_name,
            "reasoning": reasoning or "No reasoning provided",
            "parameters": parameters,
            "approved": False,
            "executed": False,
            "success": False,
            "result": None,
            "error": None,
            "dry_run": self.dry_run,
            "used_mock": False
        }
        
        # Show execution plan
        self._display_execution_plan(execution_info)
        
        # Request user approval if needed
        if not self.auto_approve:
            approved = self._request_approval(execution_info)
            execution_info["approved"] = approved
            if not approved:
                execution_info["error"] = "Execution rejected by user"
                self.execution_history.append(execution_info)
                return {
                    "success": False,
                    "error": "Execution rejected by user"
                }
        else:
            execution_info["approved"] = True
            
        # Execute the function
        if not self.dry_run:
            # Choose between real and mock implementation
            if self.use_mock and func_info["mock_func"] is not None:
                function_to_call = func_info["mock_func"]
                execution_info["used_mock"] = True
            else:
                function_to_call = func_info["func"]
            
            # Execute the function
            try:
                execution_info["executed"] = True
                
                # Show "Executing..." message
                if self.verbose:
                    print(f"\n🔄 Executing: {function_name}...")
                
                # Call the function
                result = function_to_call(*args, **kwargs)
                
                # Process the result
                execution_info["success"] = True
                execution_info["result"] = result
                
                # Log and show success
                logger.info(f"Successfully executed {function_name}")
                self._display_execution_result(execution_info)
                
                # Add to history and return
                self.execution_history.append(execution_info)
                return {
                    "success": True,
                    "result": result
                }
                
            except Exception as e:
                # Handle execution error
                execution_info["error"] = str(e)
                logger.error(f"Error executing {function_name}: {e}")
                
                # Show error
                if self.verbose:
                    print(f"\n❌ Error: {str(e)}")
                
                # Add to history and return
                self.execution_history.append(execution_info)
                return {
                    "success": False,
                    "error": str(e)
                }
        else:
            # Dry run mode - simulate success
            execution_info["success"] = True
            execution_info["result"] = f"[DRY RUN] Simulated execution of {function_name}"
            
            # Show dry run result
            if self.verbose:
                print(f"\n🔍 Dry run: {function_name} would be executed")
            
            # Add to history and return
            self.execution_history.append(execution_info)
            return {
                "success": True,
                "result": f"[DRY RUN] Simulated execution of {function_name}",
                "dry_run": True
            }
    
    def _format_parameters(self, func_info: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
        """Format function parameters for display."""
        parameters = {}
        
        # Get the function signature
        sig = func_info["signature"]
        
        # Map positional arguments to parameter names
        for i, (param_name, param) in enumerate(sig.parameters.items()):
            if i < len(args):
                parameters[param_name] = args[i]
            elif param_name in kwargs:
                parameters[param_name] = kwargs[param_name]
            elif param.default is not param.empty:
                parameters[param_name] = param.default
            else:
                parameters[param_name] = None
        
        # Add any additional keyword arguments
        for key, value in kwargs.items():
            if key not in parameters:
                parameters[key] = value
        
        return parameters
    
    def _display_execution_plan(self, execution_info: Dict[str, Any]) -> None:
        """Display the execution plan."""
        if not self.verbose:
            return
        
        function_name = execution_info["function"]
        reasoning = execution_info["reasoning"]
        parameters = execution_info["parameters"]
        
        # Format parameters as pretty JSON
        params_json = json.dumps(parameters, indent=2, default=str)
        
        # Print the execution plan
        print("\n" + "=" * 80)
        print(f"🧠 REASONING: {reasoning}")
        print("-" * 80)
        print(f"📋 FUNCTION: {function_name}")
        print(f"📝 PARAMETERS:\n{params_json}")
        print("-" * 80)
        
        # Show if using mock or dry run
        if self.dry_run:
            print("🔍 DRY RUN MODE: Function will not be executed")
        elif self.use_mock and function_name in self._function_registry and self._function_registry[function_name]["mock_func"]:
            print("🤖 MOCK MODE: Using simulated implementation")
        
        print("=" * 80)
    
    def _request_approval(self, execution_info: Dict[str, Any]) -> bool:
        """Request user approval for function execution."""
        while True:
            response = input("\n⚠️ Execute this function? (y/n): ").lower().strip()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def _display_execution_result(self, execution_info: Dict[str, Any]) -> None:
        """Display the execution result."""
        if not self.verbose:
            return
        
        function_name = execution_info["function"]
        success = execution_info["success"]
        result = execution_info["result"]
        error = execution_info["error"]
        
        print("\n" + "-" * 80)
        if success:
            print(f"✅ SUCCESS: {function_name}")
            
            # Format result as pretty JSON if possible
            try:
                if isinstance(result, (dict, list)):
                    result_str = json.dumps(result, indent=2, default=str)
                else:
                    result_str = str(result)
                
                print(f"📊 RESULT:\n{result_str}")
            except:
                print(f"📊 RESULT: {result}")
        else:
            print(f"❌ ERROR: {function_name} - {error}")
        
        print("-" * 80)
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history."""
        return self.execution_history

    def clear_execution_history(self) -> None:
        """Clear the execution history."""
        self.execution_history = []


# Global executor instance
_executor = None

def get_executor(
    auto_approve: bool = False,
    dry_run: bool = False,
    use_mock: bool = False,
    verbose: bool = True
) -> TransparentExecutor:
    """
    Get or create a global transparent executor.
    
    Args:
        auto_approve: Whether to automatically approve function calls
        dry_run: Whether to skip actual execution and just simulate
        use_mock: Whether to use mock implementations when available
        verbose: Whether to print detailed information
        
    Returns:
        TransparentExecutor: Transparent executor instance
    """
    global _executor
    
    if _executor is None:
        _executor = TransparentExecutor(
            auto_approve=auto_approve,
            dry_run=dry_run,
            use_mock=use_mock,
            verbose=verbose
        )
    
    return _executor

def wrap_function(
    func: Callable, 
    mock_func: Optional[Callable] = None
) -> Callable:
    """
    Wrap a function with transparent execution.
    
    Args:
        func: Function to wrap
        mock_func: Optional mock implementation
        
    Returns:
        Callable: Wrapped function
    """
    executor = get_executor()
    return executor.register_function(func, mock_func)


if __name__ == "__main__":
    # Example usage
    executor = get_executor(dry_run=True, verbose=True)
    
    # Define test functions
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    
    def greet(name: str) -> str:
        """Greet a person."""
        return f"Hello, {name}!"
    
    # Register functions
    wrapped_add = executor.register_function(add)
    wrapped_greet = executor.register_function(greet)
    
    # Execute functions with reasoning
    result1 = wrapped_add(3, 4, reasoning="Need to calculate the sum for further operations")
    result2 = wrapped_greet(name="Alice", reasoning="Demonstrating a greeting function")
    
    # Print execution history
    print("\nExecution History:")
    for i, entry in enumerate(executor.get_execution_history(), 1):
        print(f"\n{i}. {entry['function']} - Success: {entry['success']}") 