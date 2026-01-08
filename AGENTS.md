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

# DSPy evaluation (GPT only)
python eval_dspy.py \
  --model_name [gpt4-v|gpt|gpt-4o] \
  --task_type [scratch|tweak] \
  --task_mode [code_generation|code_edit] \
  --modalities [image_only|text_only|image+text|image+image] \
  --prompting_mode [cot|basic|few-shot] \
  --save_responses
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

# Test DSPy evaluation with single task
python test_eval_dspy.py

# Test SVG turtle integration
python test_svg_turtle.py

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
- Follow Python's PEP 8 guidelines

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
├── models/              # AI model interfaces (GPT, Gemini, LLaVA, DSPy)
│   ├── gpt.py         # OpenAI GPT interface
│   ├── gemini.py      # Google Gemini interface
│   ├── llava.py        # Replicate LLaVA interface
│   ├── dspy_models.py  # DSPy model wrappers (deprecated - GPT only in eval_dspy.py)
│   └── dspy_signatures.py # DSPy task signatures
├── utils/               # Utility modules
│   ├── code_*.py        # Code processing utilities
│   ├── shape_similarity.py
│   ├── temp_directory.py
│   └── watermark.py
├── Tasks/               # Benchmark tasks (1-131 folders)
├── autotest/source/     # Source images for testing
├── eval.py              # Main evaluation script
├── eval_dspy.py         # DSPy evaluation script (GPT only)
├── crawl_tasks.py        # Dataset generation
├── calculate_score.py    # Score calculation
└── prompts.py           # System and user prompts
```

## Development Guidelines

### Model Integration
- Each AI model has its own class in `models/` directory
- Follow the established interface: `__init__()` and `get_response()` methods
- Handle rate limiting and API errors gracefully
- Support both single and few-shot prompting modes
- For DSPy: Use standard `dspy.LM()` with predictable configuration

### Utility Functions
- Keep utility functions focused and reusable
- Use appropriate data structures (numpy arrays for images, lists for sequences)
- Follow existing patterns in `utils/` for image processing and code analysis
- SVG turtle integration is primary for headless operation

### Data Processing
- JSONL format for datasets (consistent with existing pipeline)
- Use `temp_directory.py` for temporary file management
- Follow existing patterns for image preprocessing with OpenCV
- SVG output preferred over original turtle for headless compatibility

### Testing and Validation

#### Running a Single Test
```bash
# Test DSPy evaluation with minimal parameters
python test_eval_dspy.py

# Quick turtle graphics test
python test_turtle1.py

# SVG turtle test
python test_svg_turtle.py
```

#### Manual Testing Workflow
1. Verify environment setup: `python --version`, `pip list | grep turtle`
2. Test individual components: `python -c "from svg_turtle import SvgTurtle; print('SVG turtle works')"`
3. Test with small dataset subset before full evaluation
4. Verify image generation pipeline works with new tasks
5. Check headless operation by running without display

#### Test Template
```python
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Test specific functionality
def test_functionality():
    """Test a specific feature or component."""
    try:
        # Your test code here
        print("✅ Test passed")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_functionality()
    sys.exit(0 if success else 1)
```

### Evaluation Results
- Responses saved to `.responses/` directory (gitignored)
- Reports generated in `reports/` directory
- Use `calculate_score.py` to evaluate model performance
- For DSPy: Check response structure and ChainOfThought reasoning

### Image Processing
- OpenCV for computer vision operations
- Matplotlib for visualization when needed
- Consistent image format handling across the pipeline
- SVG turtle preferred for headless operation: generates PNG directly without X11

### API Integration
- Retry logic with configurable patience and sleep time
- Proper error handling for network issues
- Base64 encoding for image inputs to models
- Rate limiting awareness for API quotas

### File Management
- Use context managers for file operations
- Clean up temporary files using `TempDirManager`
- Respect `.gitignore` patterns (don't commit `.responses/` or API keys)
- Handle both local paths and URLs for image inputs

### Configuration Notes
- Tools: Ruff configured (see `pyproject.toml`)
- No pre-commit hooks setup
- No CI/CD workflows
- DSPy integration: Use standard `dspy.LM()` pattern
- Package management: `uv` preferred over `pip`

## Common Patterns

### Image Processing
- OpenCV for computer vision operations
- Matplotlib for visualization when needed
- Consistent image format handling across the pipeline

### API Integration
- Retry logic with configurable patience and sleep time
- Proper error handling for network issues
- Base64 encoding for image inputs to models
- Rate limiting awareness for API quotas

### File Management
- Use context managers for file operations
- Clean up temporary files using `TempDirManager`
- Respect `.gitignore` patterns (don't commit `.responses/` or API keys)

### DSPy Integration
- Standard `dspy.LM()` with model-specific configuration
- `dspy.ChainOfThought()` for reasoning-based generation
- `dspy.configure()` for global model setup
- Use `dspy.context()` for execution context management
- Fallback to original model interface if DSPy prediction fails

### Model-Specific Patterns

#### GPT Models
- Use `openai/gpt-4o` for latest capabilities
- Handle rate limits with patience and backoff
- Support both `gpt-4o`, `gpt`, and `gpt4-v` identifiers
- API key from `OPENAI_API_KEY` environment variable

#### Gemini Models
- Use `google.generativeai` library
- Support `gemini-1.5-flash` for faster inference
- Handle content policy restrictions
- API key from `GOOGLE_API_KEY` environment variable

#### LLaVA Models
- Use Replicate API for multimodal models
- Handle different LLaVA variants
- Support image + text inputs
- API key from `REPLICATE_API_TOKEN` environment variable

### SVG Turtle Integration
- Use `svg_turtle` for headless graphics generation
- `cairosvg` for SVG to PNG conversion
- Fallback to original turtle if SVG processing fails
- Transform turtle code automatically: remove imports, replace method calls
- Handle method name differences: `pensize()` → `width()`, `done()` → commented out

### Code Generation
- Prompt templates in `prompts.py` for consistency
- System messages for role definition and behavior guidance
- User prompts with placeholder formatting for dynamic content
- Support for chain-of-thought reasoning with DSPy

### Benchmark Evaluation
- Task filtering by type (scratch/tweak) and question number
- Accuracy calculation using shape similarity
- Progress tracking with tqdm
- Report generation in standardized format
- Support for both absolute and relative accuracy metrics

## Key Implementation Files

### Core Evaluation Scripts
- `eval.py` - Original evaluation with model-specific classes
- `eval_dspy.py` - DSPy-based evaluation (GPT only, simplified)

### Model Interfaces
- `models/gpt.py` - OpenAI GPT integration
- `models/gemini.py` - Google Gemini integration  
- `models/llava.py` - LLaVA integration via Replicate

### Utilities
- `utils/code_to_image.py` - Main image generation (now SVG-first)
- `utils/code_to_image_svg.py` - SVG turtle specific implementation
- `utils/shape_similarity.py` - Shape-based accuracy calculation
- `utils/temp_directory.py` - Temporary file management
- `utils/watermark.py` - Image watermarking for code_edit tasks

### Data Processing
- `prompts.py` - System and user prompt templates
- `crawl_tasks.py` - Dataset generation from Tasks directory
- `calculate_score.py` - Performance evaluation and reporting

## Troubleshooting

### Common Issues
- **Display errors**: Use SVG turtle for headless operation
- **API rate limits**: Increase patience and sleep_time in model initialization
- **Module import errors**: Ensure virtual environment is activated
- **Missing dependencies**: Run `uv pip install -r requirements.txt`
- **SVG conversion failures**: Check `cairosvg` installation and image permissions

### Debug Commands
```bash
# Test model connection
python -c "from models.gpt import GPTModel; import os; model = GPTModel(os.getenv('OPENAI_API_KEY')); print('GPT model initialized')"

# Test SVG turtle
python -c "from svg_turtle import SvgTurtle; t = SvgTurtle(100, 100); t.forward(50); print('SVG turtle working')"

# Test DSPy configuration  
python -c "import dspy; lm = dspy.LM(model='openai/gpt-4o'); print('DSPy LM initialized')"
```

### Log Analysis
- Check model response patterns for consistent formatting
- Monitor accuracy trends across different parameter combinations
- Review failure cases for prompt improvement opportunities
- Track API usage and cost patterns

## Performance Optimization

### Code Generation Speed
- Use DSPy ChainOfThought for structured reasoning
- Implement caching for repeated computations
- Optimize image preprocessing pipeline
- Consider model-specific optimizations (token limits, context windows)

### Memory Management
- Clean up temporary files promptly
- Use generators for large dataset processing
- Implement streaming for large response handling
- Monitor memory usage during batch operations

### Scalability Considerations
- Parallel processing for independent tasks
- Batch API requests when supported
- Efficient image loading and preprocessing
- Consider distributed evaluation for large datasets

## Security and Best Practices

### API Key Management
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly in production environments
- Implement key validation before API usage

### Code Security
- Validate all user inputs and parameters
- Sanitize file paths and external data
- Implement input length limits and content validation
- Use safe evaluation practices for generated code

### Data Privacy
- Handle user data according to privacy requirements
- Implement data retention policies
- Use anonymization for evaluation data when needed
- Follow GDPR/CCPA guidelines for user data

## Updates and Maintenance

### Version Management
- Semantic versioning following MAJOR.MINOR.PATCH pattern
- Maintain CHANGELOG.md for significant changes
- Tag releases appropriately
- Document breaking changes clearly

### Testing Updates
- Add new tests for added functionality
- Update existing tests for compatibility
- Maintain test coverage metrics
- Test with multiple Python versions

### Documentation Updates
- Update AGENTS.md for new development patterns
- Maintain README.md with current capabilities
- Add code examples for new features
- Document configuration options and environment variables

When adding new functionality, maintain consistency with existing patterns and consider suggesting improvements to the development tooling and evaluation methodologies.