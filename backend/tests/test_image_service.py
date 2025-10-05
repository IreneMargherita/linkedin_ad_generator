"""
Unit tests for ImageService.
"""
import pytest
from unittest.mock import Mock, patch
from service.image_service import ImageService
from dto.ad_form_dto import AdFormData


class TestImageService:
    """Test cases for ImageService."""

    def test_init(self, mock_prompt_service, mock_image_generator):
        """Test ImageService initialization."""
        service = ImageService(mock_prompt_service, mock_image_generator)
        assert service.prompt_service == mock_prompt_service
        assert service.image_generator == mock_image_generator

    def test_generate_ad_image_success(self, mock_prompt_service, mock_image_generator, sample_ad_form_data):
        """Test successful image generation."""
        # Arrange
        service = ImageService(mock_prompt_service, mock_image_generator)
        style = "minimalist design"
        image_number = 1
        
        expected_prompt = "Generated prompt for image"
        mock_prompt_service.build_prompt.return_value = expected_prompt
        
        expected_result = {
            "success": True,
            "imageData": "base64_image_data",
            "imageNumber": image_number,
            "prompt": expected_prompt
        }
        mock_image_generator.generate.return_value = expected_result

        # Act
        result = service.generate_ad_image(sample_ad_form_data, style, image_number)

        # Assert
        mock_prompt_service.build_prompt.assert_called_once_with(sample_ad_form_data, style)
        mock_image_generator.generate.assert_called_once_with(expected_prompt, image_number)
        assert result == expected_result

    def test_generate_ad_image_prompt_service_error(self, mock_prompt_service, mock_image_generator, sample_ad_form_data):
        """Test image generation when prompt service fails."""
        # Arrange
        service = ImageService(mock_prompt_service, mock_image_generator)
        mock_prompt_service.build_prompt.side_effect = Exception("Prompt service error")

        # Act & Assert
        with pytest.raises(Exception, match="Prompt service error"):
            service.generate_ad_image(sample_ad_form_data, "style", 1)

    def test_generate_ad_image_generator_error(self, mock_prompt_service, mock_image_generator, sample_ad_form_data):
        """Test image generation when image generator fails."""
        # Arrange
        service = ImageService(mock_prompt_service, mock_image_generator)
        mock_prompt_service.build_prompt.return_value = "test prompt"
        mock_image_generator.generate.side_effect = Exception("Generator error")

        # Act & Assert
        with pytest.raises(Exception, match="Generator error"):
            service.generate_ad_image(sample_ad_form_data, "style", 1)

    def test_generate_ad_image_with_different_parameters(self, mock_prompt_service, mock_image_generator):
        """Test image generation with various parameter combinations."""
        # Arrange
        service = ImageService(mock_prompt_service, mock_image_generator)
        
        test_cases = [
            {
                "form_data": AdFormData(
                    companyUrl="https://test1.com",
                    productName="Product 1",
                    businessValue="Value 1",
                    audience="Audience 1",
                    bodyText="Body 1",
                    footerText="Footer 1"
                ),
                "style": "style 1",
                "image_number": 1
            },
            {
                "form_data": AdFormData(
                    companyUrl="https://test2.com",
                    productName="Product 2",
                    businessValue="Value 2",
                    audience="Audience 2",
                    bodyText="Body 2",
                    footerText="Footer 2"
                ),
                "style": "style 2",
                "image_number": 2
            }
        ]

        for case in test_cases:
            # Reset mocks
            mock_prompt_service.reset_mock()
            mock_image_generator.reset_mock()
            
            # Setup
            mock_prompt_service.build_prompt.return_value = f"prompt for {case['image_number']}"
            mock_image_generator.generate.return_value = {
                "success": True,
                "imageData": f"image_{case['image_number']}",
                "imageNumber": case['image_number'],
                "prompt": f"prompt for {case['image_number']}"
            }

            # Act
            result = service.generate_ad_image(
                case["form_data"],
                case["style"],
                case["image_number"]
            )

            # Assert
            mock_prompt_service.build_prompt.assert_called_once_with(
                case["form_data"], case["style"]
            )
            mock_image_generator.generate.assert_called_once_with(
                f"prompt for {case['image_number']}", case["image_number"]
            )
            assert result["success"] is True
            assert result["imageNumber"] == case["image_number"]
