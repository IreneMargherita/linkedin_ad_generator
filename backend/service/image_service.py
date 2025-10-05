import os
import base64
import logging
from openai import OpenAI
from dotenv import load_dotenv
from dto.ad_form_dto import AdFormData
from interfaces.prompt_service_interface import PromptServiceInterface
from interfaces.image_generator_interface import ImageGeneratorInterface

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self, prompt_service: PromptServiceInterface, image_generator: ImageGeneratorInterface):
        self.prompt_service = prompt_service
        self.image_generator = image_generator
    def generate_ad_image(self, form_data: AdFormData, style: str, image_number: int) -> dict:
        logger.info(f"Starting image generation for image #{image_number}")
        prompt = self.prompt_service.build_prompt(form_data, style)
        return self.image_generator.generate(prompt, image_number)
