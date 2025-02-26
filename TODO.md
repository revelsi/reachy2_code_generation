# TODO: Reachy Function Calling Project

## Current Issues

1. **LangGraph Agent Implementation Issues**:
   - Fixed: `get_available_tools` method was trying to call `.values()` on a list object
   - The agent is loading 0 tools and 0 implementations, indicating the tool discovery process is not working
   - The agent is running in mock mode (`Use mock: True` in configuration)

2. **Testing Setup**:
   - The test script (`test_agent.py`) was created but may need adjustments
   - Mock WebSocket server implementation may need review
   - Need to ensure tests can run without affecting the main application

3. **Tool Mapper Integration**:
   - The `ReachyToolMapper` class in `agent/tool_mapper.py` is implemented but tools aren't being discovered
   - Need to verify the tool discovery and registration process

4. **WebSocket Notifications**:
   - WebSocket server is initialized but may need further testing

## Action Items

### High Priority

1. **Fix Tool Discovery**:
   - Debug why `ReachyToolMapper` is not finding any tools
   - Check the tool directory structure and ensure tools are in the expected location
   - Verify that tool classes follow the expected format for discovery

2. **Fix Agent Initialization**:
   - Ensure the agent properly initializes with tools
   - Review the `load_tools` method in `ReachyLangGraphAgent`

3. **Configuration Management**:
   - Review how mock mode is configured and ensure it can be toggled appropriately
   - Document the configuration options in README.md

### Medium Priority

1. **Testing Infrastructure**:
   - Complete the testing setup to allow isolated testing of the agent
   - Create comprehensive test cases for different agent behaviors
   - Ensure tests can run without requiring actual robot hardware

2. **Error Handling**:
   - Improve error handling throughout the application
   - Add more detailed logging to help diagnose issues

3. **Documentation**:
   - Update documentation to reflect the current state of the project
   - Document the LangGraph implementation and how it differs from previous approaches

### Low Priority

1. **Code Cleanup**:
   - Review and refactor code for clarity and maintainability
   - Remove any unused or deprecated code

2. **Performance Optimization**:
   - Identify and address any performance bottlenecks
   - Consider caching mechanisms for frequently used data

## Notes for Next Session

- Start by fixing the tool discovery issue
- Test the agent with mock tools before attempting to use real hardware
- Consider creating a simplified version of the agent for testing purposes
- Review the LangGraph documentation to ensure our implementation follows best practices

## References

- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- OpenAI function calling documentation: https://platform.openai.com/docs/guides/function-calling 