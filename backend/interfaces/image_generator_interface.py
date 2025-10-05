
from abc import ABC, abstractmethod

class ImageGeneratorInterface(ABC):
    """Abstract interface for any image generation provider."""

    @abstractmethod
    def generate(self, prompt: str, image_number: int) -> dict:
        """Generate an image and return metadata (success, base64, etc.)."""
        pass
