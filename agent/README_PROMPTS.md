# Unified Prompt Building System

This document outlines the unified prompt building system for the Reachy 2 Code Generation project. This system provides a modular and maintainable way to build prompts for both the code generator and code evaluator components.

## Overview

The prompt building system is designed to:

1. **Share common content** between generator and evaluator prompts
2. **Avoid duplication** of critical information
3. Provide a **single source of truth** for prompt sections
4. Allow for **easy updates** when API changes occur
5. Support **customization** of prompt order and content

## System Structure

The system is implemented in `prompt_config.py` and consists of:

1. **Section Variables** - Text blocks representing different parts of the prompts
2. **Section Collection Functions** - Functions that gather all sections for a specific prompt type
3. **Section Order Functions** - Functions that define the default order of sections
4. **Prompt Builder Functions** - Functions that build complete prompts from sections

## Common vs. Specific Sections

The system identifies two types of sections:

- **Common Sections** - Shared between generator and evaluator (prefixed with "shared_" in evaluator prompt)
  - API documentation
  - Critical warnings
  - Code structure requirements
  - Workspace safety guidelines
  
- **Specific Sections** - Unique to either generator or evaluator
  - Generator: Role definition, response format
  - Evaluator: Evaluation criteria, scoring guidelines, feedback format

## How to Use

### Building a Generator Prompt

```python
from agent.prompt_config import build_generator_prompt

# Build with default section order
prompt = build_generator_prompt()

# Build with custom section order
custom_order = ["core_role", "critical_warnings", "api_summary", "response_format"]
prompt = build_generator_prompt(custom_order=custom_order)
```

### Building an Evaluator Prompt

```python
from agent.prompt_config import build_evaluator_prompt

# Build with default section order
prompt = build_evaluator_prompt()

# Build with custom section order
custom_order = ["evaluator_core_role", "shared_critical_warnings", "evaluation_criteria"]
prompt = build_evaluator_prompt(custom_order=custom_order)
```

## How to Maintain

### Updating Existing Sections

To update an existing section:

1. Find the section variable in `prompt_config.py` (e.g., `CRITICAL_WARNINGS_SIMPLIFIED`)
2. Edit the content while maintaining the same format and structure
3. All prompts using that section will automatically use the updated content

### Adding New Sections

To add a new section:

1. Define a new variable in `prompt_config.py` with the content
2. Add the section to the appropriate section collection function:
   - Generator: Add to `get_prompt_sections()`
   - Evaluator: Add to `get_evaluator_prompt_sections()`
3. Optionally update the default order in `get_default_prompt_order()` or `get_default_evaluator_prompt_order()`

### Synchronizing Changes

When making changes that affect both generator and evaluator:

1. Update the common sections in the generator part of the file
2. The evaluator will automatically use the updated common sections

## Best Practices

1. **Keep Sections Focused**: Each section should address a specific aspect of the prompt
2. **Maintain Format Consistency**: Use consistent formatting within sections
3. **Update Documentation**: When adding/modifying sections, update this README
4. **Test Changes**: After updating, test both generator and evaluator functionality
5. **Preserve Section Names**: Changing section names requires updating references in code

## Example: Adding a New Section

```python
# 1. Define the new section
NEW_SECTION = """
NEW SECTION CONTENT:
- Point 1
- Point 2
"""

# 2. Add to the appropriate collection function
def get_prompt_sections():
    # Existing code...
    return {
        # Existing sections...
        "new_section": NEW_SECTION,
    }

# 3. Optionally update the default order
def get_default_prompt_order():
    return [
        # Existing order...
        "new_section",
    ]
``` 