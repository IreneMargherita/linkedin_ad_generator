import os
import logging
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv
from interfaces.image_generator_interface import ImageGeneratorInterface

load_dotenv()
logger = logging.getLogger(__name__)

class OpenAIImageGeneratorService(ImageGeneratorInterface):
    def __init__(self, client=None):
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            self.client = client or OpenAI(api_key=api_key)
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            raise

    def generate(self, prompt: str, image_number: int) -> dict:
        """Generate an image using OpenAI's gpt-image-1 with safe error handling."""
        logger.info(f"Generating image #{image_number} via OpenAI gpt-image-1")

        try:
            # Attempt image generation
            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024"
            )

            # Safely extract image data
            if not hasattr(response, "data") or not response.data:
                raise ValueError("Invalid response format: no data found in response.")

            image_base64 = response.data[0].b64_json

            return {
                "success": True,
                "imageData": image_base64,
                "imageNumber": image_number,
                "prompt": prompt
            }

        except (APIError, APIConnectionError, RateLimitError) as api_err:
            logger.error(f"OpenAI API error for image #{image_number}: {api_err}")
            return {
                "success": False,
                "error": f"OpenAI API error: {str(api_err)}",
                "imageNumber": image_number
            }

        except ValueError as val_err:
            logger.error(f"Value error while generating image #{image_number}: {val_err}")
            return {
                "success": False,
                "error": str(val_err),
                "imageNumber": image_number
            }

        except Exception as e:
            logger.exception(f"Unexpected error while generating image #{image_number}: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "imageNumber": image_number
            }
