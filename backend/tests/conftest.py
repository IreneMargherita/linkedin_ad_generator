import pytest
from unittest.mock import Mock
from dto.ad_form_dto import AdFormData


@pytest.fixture
def mock_prompt_service():
    """Mock prompt service fixture."""
    service = Mock()
    service.build_prompt = Mock()
    return service


@pytest.fixture
def mock_image_generator():
    """Mock image generator fixture."""
    generator = Mock()
    generator.generate = Mock()
    return generator


@pytest.fixture
def sample_ad_form_data():
    """Sample ad form data fixture."""
    return AdFormData(
        companyUrl="https://example.com",
        productName="Test Product",
        businessValue="Boost productivity",
        audience="Tech professionals",
        bodyText="Experience seamless workflow with our tool.",
        footerText="Join 10k+ happy customers!"
    )


@pytest.fixture
def mock_openai_response():
    """Mock response object for OpenAI image generation."""
    mock_response = Mock()
    mock_response.data = [Mock(b64_json="fake_base64_image_data")]
    return mock_response
