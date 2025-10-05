# Test Suite for LinkedIn Ad Generator Backend

This directory contains tests for the LinkedIn Ad Generator backend application.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_image_service.py       # Unit tests for ImageService
├── test_openai_image_generator_service.py  # Unit tests for OpenAI image generator
└── README.md                   # This file
```

```bash
# Run all tests
pytest
# Run with coverage report
pytest --cov=. --cov-report=html
```
### Running Specific Test Files

```bash
# Run specific test file
pytest tests/test_image_service.py

# Run specific test class
pytest tests/test_image_service.py::TestImageService

# Run specific test method
pytest tests/test_image_service.py::TestImageService::test_generate_ad_image_success
```
### Unit Tests
- **test_image_service.py**: Tests for the ImageService class
  - Service initialization
  - Successful image generation
  - Error handling for prompt service failures
  - Error handling for image generator failures
  - Different parameter combinations
- **test_openai_image_generator_service.py**: Tests for OpenAI image generation
  - Service initialization 
  - Successful image generation
  - Rate limit error handling
  - Invalid response format handling
  - Empty response data handling
  - Unexpected error handling
  - Different parameter combinations


