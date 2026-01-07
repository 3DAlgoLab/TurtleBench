# TurtleBench - Agent Development Guide

This guide is for agentic coding assistants working on the TurtleBench visual programming benchmark project.

## Project Overview

TurtleBench is a research benchmark for evaluating Large Multimodal Models (LMMs) on geometric pattern understanding and Python Turtle code generation. It consists of 131 tasks with varying complexity across multiple modalities.

## Environment Setup

### Python Version
- Use Python 3.12 (specified in `.python-version`)
- Preferred package manager: `uv` (with `uv.lock` present)
- Fallback: `pip` with `requirements.txt`

### Installation Commands
```bash
# Using uv (preferred)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
- Copy `.env.example` to `.env` and add API keys for OpenAI, Google AI, etc.
- Required: `OPENAI_API_KEY`, `GOOGLE_API_KEY` for model evaluations

## Core Commands

### Model Evaluation
```bash
# Main evaluation script
python eval.py \
  --model_name [gemini|gpt|llava] \
  --task_type [scratch|tweak] \
  --task_mode [code_generation|code_edit] \
  --modalities [image_only|text_only|image+text|image+image] \
  --prompting_mode [cot|basic|few-shot] \
  --save_responses

# Example: GPT-4o on scratch tasks with images
python eval.py --model_name gpt --task_type scratch --modalities image_only --prompting_mode cot --save_responses
```

### Dataset Management
```bash
# Generate dataset from Tasks directory
python crawl_tasks.py

# Calculate scores from model responses
python calculate_score.py
```

### Testing
```bash
# Basic turtle graphics test
python test_turtle1.py

# Test specific functionality (add your own tests)
# Currently no automated test framework configured
```

## Code Style Guidelines

### Import Style
- Standard library imports first: `import os`, `import json`
- Third-party imports next: `import cv2`, `from openai import OpenAI`
- Local imports last: `from models.gpt import GPTModel`, `from utils.shape_similarity import calculate_accuracy`
- Group related imports together
- Use absolute imports for local modules

### Formatting Conventions
- Indentation: 4 spaces (no tabs)
- Line length: Aim for under 100 characters when reasonable
- Blank lines between functions and classes
- No trailing whitespace

### Naming Conventions
- **Classes**: PascalCase (`GPTModel`, `GeminiModel`, `LlavaModel`)
- **Functions/Variables**: snake_case (`calculate_accuracy`, `encode_image`, `task_mode`)
- **Constants**: UPPER_SNAKE_CASE (rare, but use for configuration values)
- **Private methods**: prefix with underscore (`_preprocess_code`)

### Class Structure
```python
class ModelName:
    def __init__(self, api_key, patience=5, sleep_time=1) -> None:
        # Initialize instance variables
        
    def get_response(self, system_message, user_message, base_image, result_image):
        # Main method for model interaction
```

### Error Handling
- Use try-except blocks for API calls and file operations
- Raise custom exceptions from `utils.run_option_error.py` when appropriate
- Use assert statements for input validation in critical functions
- Log errors appropriately for debugging model interactions

### Function Documentation
- Currently minimal documentation style in codebase
- Add docstrings for new complex functions following this pattern:
```python
def function_name(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
```

## Project Structure

```
TurtleBench/
├── models/              # AI model interfaces (GPT, Gemini, LLaVA)
├── utils/               # Utility modules
│   ├── code_*.py        # Code processing utilities
│   ├── shape_similarity.py
│   └── temp_directory.py
├── Tasks/               # Benchmark tasks (1-131 folders)
├── autotest/source/     # Source images for testing
├── eval.py              # Main evaluation script
├── crawl_tasks.py       # Dataset generation
├── calculate_score.py   # Score calculation
└── prompts.py           # System and user prompts
```

## Development Guidelines

### Model Integration
- Each AI model has its own class in `models/` directory
- Follow the established interface: `__init__()` and `get_response()` methods
- Handle rate limiting and API errors gracefully
- Support both single and few-shot prompting modes

### Utility Functions
- Keep utility functions focused and reusable
- Use appropriate data structures (numpy arrays for images, lists for sequences)
- Follow existing patterns in `utils/` for image processing and code analysis

### Data Processing
- JSONL format for datasets (consistent with existing pipeline)
- Use `temp_directory.py` for temporary file management
- Follow existing patterns for image preprocessing with OpenCV

## Testing and Validation

### Manual Testing
- Use `test_turtle1.py` for basic turtle graphics validation
- Test model integrations with small task subsets before full evaluation
- Verify image generation pipeline works with new tasks

### Evaluation Results
- Responses saved to `.responses/` directory (gitignored)
- Reports generated in `reports/` directory
- Use `calculate_score.py` to evaluate model performance

## Common Patterns

### Image Processing
- OpenCV for computer vision operations
- Matplotlib for visualization when needed
- Consistent image format handling across the pipeline

### API Integration
- Retry logic with configurable patience and sleep time
- Proper error handling for network issues
- Base64 encoding for image inputs to models

### File Management
- Use context managers for file operations
- Clean up temporary files using `TempDirManager`
- Respect `.gitignore` patterns (don't commit `.responses/` or API keys)

## Configuration Notes

- No linting tools currently configured (consider adding Black/Ruff)
- No pre-commit hooks setup
- No CI/CD workflows
- `pyproject.toml` has minimal configuration

When adding new functionality, maintain consistency with existing patterns and consider suggesting improvements to the development tooling.