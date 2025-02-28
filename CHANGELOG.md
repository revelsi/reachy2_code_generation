# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Development environment setup scripts (`start_dev.sh` and `start_dev.bat`) for consistent environment setup
- Tool verification script (`verify_tools.py`) to check tool generation
- Comprehensive test suite for tool functionality
- CONTRIBUTING.md with guidelines for contributors
- CHANGELOG.md to track changes
- Improved .gitignore patterns for generated files
- Added detailed documentation for using generated tools in README.md
- Added tool execution result notifications via WebSocket
- Added error message display with auto-fade in the web interface
- Added new connection manager module for centralized Reachy connection handling
- Added dual-mode architecture supporting both function calling and code generation
- Added code generation agent for translating natural language to Python code
- Added basic code validation framework for generated code
- Added centralized model configuration management system
- Added UI components for switching between modes and configuring model parameters
- Added CLI support for dual-mode operation
- Added test script for verifying model configuration functionality

### Fixed
- Tool discovery and generation now working correctly (208 tools loaded)
- Fixed `load_api_documentation` method to handle API documentation as a list of dictionaries
- Updated import paths for the reorganized directory structure
- Tool implementations now have proper error handling and consistent return formats
- Fixed WebSocket server to properly notify clients of tool execution and results
- Fixed connection handling in tool implementations to use centralized connection manager
- Fixed import issues in generated tool files

### Changed
- Moved utility files to the `agent/utils` directory for better organization
- Updated README.md to reflect the current state of the project
- Updated TODO.md to mark completed items and add new tasks
- Improved WebSocket message handling in the frontend
- Refactored tool generation to use consistent connection pattern
- Migrated from `get_reachy_connection` to `get_reachy` for better connection management
- Refactored API endpoints to support dual-mode architecture
- Enhanced web interface to support both function calling and code generation modes
- Restructured agent initialization to use centralized model configuration

## [0.1.0] - 2023-02-26

### Added
- Initial project structure
- LangGraph agent implementation
- Mock robot implementation
- Web interface for interacting with the robot
- REST API for controlling the robot
- WebSocket server for real-time updates
- Tool mapper for discovering and registering tools
- SDK documentation scraper 