from service.image_service import ImageService
from service.linkedin_prompt_service import LinkedInPromptService
from service.openai_image_generator_service import OpenAIImageGeneratorService

def get_Linkedin_openai_image_service() -> ImageService:
    """Factory for dependency injection."""
    prompt_service = LinkedInPromptService()  
    image_generator = OpenAIImageGeneratorService()
    return ImageService(prompt_service, image_generator)
 