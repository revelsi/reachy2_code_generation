# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.3] - 2025-04-16

### Added
- Support for OpenAI O-family models (o1, o1-mini, o3, o3-mini) with specific configuration parameters (`reasoning_effort`, `max_completion_tokens`).

### Changed
- Refactored configuration loading (`config.py`) to handle distinct parameter sets for different model families.

## [1.0.2] - 2025-04-15

### Added
- New conversational chat interface for more intuitive code generation
- Full chat history support with back-and-forth conversation capabilities
- Improved typography and layout for better reading experience

### Improved
- Optimized performance with API documentation caching to prevent redundant loading
- Streamlined interface with cleaner feedback presentation
- Enhanced user experience with responsive chat interactions
- Strengthened code evaluation with stricter scoring rules and safety focus in the prompt

## [1.0.1] - 2025-04-14

### Improved
- Completely redesigned UI with a modern two-column layout for better usability
- Updated code editor with Source Code Pro font for improved readability
- Fixed execution feedback display to only show loading animation during execution, not code generation
- Simplified status indicators with clear visual feedback for different states
- Improved error handling and status messaging throughout the interface

## [1.0.0] - 2025-04-08

### Added
- Initial public release of the Reachy2 code generation system
- Gradio interface for code generation with real-time status updates
- Code validation framework for generated Python code
- Support for natural language to Python code translation
- Robot connection status indicator
- Simple launcher script (launch_code_gen.py) for easy access

### Features
- Natural language to Python code translation for Reachy2 robot control
- Code validation to ensure generated code is executable
- Real-time status updates during code generation process
- User-friendly interface for robot interaction
- Comprehensive error handling for common robot control errors 