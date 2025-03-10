## Features

- **Natural Language to Code**: Convert natural language descriptions into executable Python code for the Reachy 2 robot
- **Real-time Status Updates**: See the current status of the code generation process
- **Automatic Code Validation**: Validate generated code before execution
- **Recursive Code Correction**: Automatically fix common issues in the generated code (up to 3 attempts)
- **Correction History**: View a history of what issues were fixed during code generation
- **Code Execution**: Execute the generated code directly from the interface
- **Detailed Feedback**: Get detailed feedback about code execution results
- **Robot Connection Status**: See if the Reachy robot or simulator is available
- **Transparent Validation Process**: Clear explanation of the validation steps and results

## Model

The interface uses **GPT-4o-mini**, which is optimized for Reachy 2 code generation. This model provides a good balance between performance and cost efficiency, making it ideal for generating code for the Reachy 2 robot.

## Code Validation Process

When code is generated, it goes through these validation steps:

1. **Syntax Check**: Ensures the code has valid Python syntax
2. **Import Validation**: Verifies all imports are available
3. **API Usage Check**: Confirms correct usage of the Reachy API
4. **Safety Check**: Looks for potentially harmful operations

When issues are found, the model will attempt to fix them automatically (up to 3 correction attempts). The interface provides transparency about this process, showing:
- What issues were found
- Whether they were successfully fixed
- A detailed correction history

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