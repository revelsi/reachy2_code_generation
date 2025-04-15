## Features

- **Natural Language to Code**: Convert natural language descriptions into executable Python code for the Reachy 2 robot
- **Real-time Status Updates**: See the current status of the code generation process
- **Automatic Code Validation**: Validate generated code before execution
- **Code Execution**: Execute the generated code directly from the interface
- **Detailed Feedback**: Get detailed feedback about code execution results
- **Robot Connection Status**: See if the Reachy robot or simulator is available
- **Transparent Validation Process**: Clear explanation of the validation steps and results

## Model

### Model Configuration

The interface uses **gpt-4.1-mini** as the default generator model and **gpt-4.1-nano** as the default evaluator model. These models provide a good balance between performance and cost efficiency, making them ideal for generating code for the Reachy 2 robot.

## Code Validation Process

When code is generated, it goes through these validation steps:

1. **Syntax Check**: Ensures the code has valid Python syntax
2. **Import Validation**: Verifies all imports are available
3. **API Usage Check**: Confirms correct usage of the Reachy API
   - Validates proper gripper access through arm properties (e.g., `arm.gripper`)
   - Checks for incorrect patterns like `r_gripper`, `l_gripper`, or `gripper()`
4. **Safety Check**: Looks for potentially harmful operations

The interface provides transparency about this process, showing what issues were found in the validation results.

### Common API Usage Examples

```python
# Correct gripper access
reachy.r_arm.gripper.open()           # ✅ Correct: Access gripper as a property
reachy.l_arm.gripper.set_opening(0.5) # ✅ Correct: Access gripper as a property

# Incorrect gripper access
reachy.r_gripper.open()               # ❌ Wrong: Direct gripper access
reachy.l_arm.gripper().close()        # ❌ Wrong: Calling gripper as a method
```

### Command-line Arguments

You can customize the interface with the following command-line arguments:

- `--temperature`: The temperature parameter for the model (default: 0.2)
- `--max-tokens`: The maximum number of tokens to generate (default: 4000)
- `--port`: The port to run the server on (default: 7860)
- `--websocket-port`: The port for the WebSocket server (default: 8765)
- `--share`: Create a public link to share the interface

Example:

```bash
python launch_code_gen.py --temperature 0.3 --max-tokens 5000 --port 7861 --websocket-port 8766
``` 