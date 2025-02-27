# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite for tool functionality
- CONTRIBUTING.md with guidelines for contributors
- CHANGELOG.md to track changes
- Improved .gitignore patterns for generated files

### Fixed
- Tool discovery and generation now working correctly (208 tools loaded)
- Fixed `load_api_documentation` method to handle API documentation as a list of dictionaries
- Updated import paths for the reorganized directory structure
- Tool implementations now have proper error handling and consistent return formats

### Changed
- Moved utility files to the `agent/utils` directory for better organization
- Updated README.md to reflect the current state of the project
- Updated TODO.md to mark completed items and add new tasks

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