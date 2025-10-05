"""
Unit tests for OpenAIImageGeneratorService.
"""
import pytest
from unittest.mock import Mock, patch
from openai import APIError, APIConnectionError, RateLimitError
from service.openai_image_generator_service import OpenAIImageGeneratorService


class TestOpenAIImageGeneratorService:
    """Test cases for OpenAIImageGeneratorService."""

    def test_init_success(self):
        """Test successful initialization."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('service.openai_image_generator_service.OpenAI') as mock_openai:
                mock_client = Mock()
                mock_openai.return_value = mock_client
                
                service = OpenAIImageGeneratorService()
                
                assert service.client == mock_client
                mock_openai.assert_called_once_with(api_key='test-key')

    def test_init_with_custom_client(self):
        """Test initialization with custom client."""
        custom_client = Mock()
        service = OpenAIImageGeneratorService(client=custom_client)
        assert service.client == custom_client

    def test_init_missing_api_key(self):
        """Test initialization with missing API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
                OpenAIImageGeneratorService()

    def test_generate_success(self, mock_openai_response):
        """Test successful image generation."""
        # Arrange
        mock_client = Mock()
        mock_client.images.generate.return_value = mock_openai_response
        service = OpenAIImageGeneratorService(client=mock_client)
        
        prompt = "Test prompt"
        image_number = 1

        # Act
        result = service.generate(prompt, image_number)

        # Assert
        mock_client.images.generate.assert_called_once_with(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        assert result["success"] is True
        assert result["imageData"] == mock_openai_response.data[0].b64_json
        assert result["imageNumber"] == image_number
        assert result["prompt"] == prompt


    def test_generate_rate_limit_error(self):
        """Test image generation with rate limit error."""
        # Arrange
        mock_client = Mock()
        mock_client.images.generate.side_effect = RateLimitError("Rate limit exceeded", response=Mock(), body={})
        service = OpenAIImageGeneratorService(client=mock_client)

        # Act
        result = service.generate("test prompt", 1)

        # Assert
        assert result["success"] is False
        assert "OpenAI API error" in result["error"]
        assert result["imageNumber"] == 1

    def test_generate_invalid_response_format(self):
        """Test image generation with invalid response format."""
        # Arrange
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = None  # Invalid response
        mock_client.images.generate.return_value = mock_response
        service = OpenAIImageGeneratorService(client=mock_client)

        # Act
        result = service.generate("test prompt", 1)

        # Assert
        assert result["success"] is False
        assert "Invalid response format" in result["error"]
        assert result["imageNumber"] == 1

    def test_generate_empty_response_data(self):
        """Test image generation with empty response data."""
        # Arrange
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = []  # Empty data
        mock_client.images.generate.return_value = mock_response
        service = OpenAIImageGeneratorService(client=mock_client)

        # Act
        result = service.generate("test prompt", 1)

        # Assert
        assert result["success"] is False
        assert "Invalid response format" in result["error"]
        assert result["imageNumber"] == 1

    def test_generate_unexpected_error(self):
        """Test image generation with unexpected error."""
        # Arrange
        mock_client = Mock()
        mock_client.images.generate.side_effect = Exception("Unexpected error")
        service = OpenAIImageGeneratorService(client=mock_client)

        # Act
        result = service.generate("test prompt", 1)

        # Assert
        assert result["success"] is False
        assert "Unexpected error" in result["error"]
        assert result["imageNumber"] == 1

    def test_generate_with_different_parameters(self):
        """Test image generation with various parameters."""
        # Arrange
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].b64_json = "test_image_data"
        mock_client.images.generate.return_value = mock_response
        service = OpenAIImageGeneratorService(client=mock_client)

        test_cases = [
            ("Short prompt", 1),
            ("Very long prompt with lots of details and specifications", 2),
            ("", 3),  # Empty prompt
            ("Prompt with special characters: !@#$%^&*()", 4)
        ]

        for prompt, image_number in test_cases:
            # Reset mock
            mock_client.reset_mock()
            
            # Act
            result = service.generate(prompt, image_number)

            # Assert
            mock_client.images.generate.assert_called_once_with(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024"
            )
            assert result["success"] is True
            assert result["imageNumber"] == image_number
            assert result["prompt"] == prompt
