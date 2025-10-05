import logging
from fastapi import HTTPException
from dto.ad_form_dto import ImageGenerationRequest, ImageGenerationResponse
from service.image_service import ImageService

logger = logging.getLogger(__name__)


class AdController:
    """Controller for handling ad generation requests."""

    def __init__(self, image_service: ImageService):
        self.image_service = image_service

    async def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Process image generation request and format the response."""
        logger.info(f"Image generation request received (image #{request.imageNumber})")

        try:
            result = self.image_service.generate_ad_image(
                form_data=request.formData,
                style=request.style,
                image_number=request.imageNumber
            )

            if result["success"]:
                logger.info(f"Image generation successful for image #{request.imageNumber}")
                logger.info(f"Final score: {result.get('final_score', 'N/A')}, Iterations: {result.get('iterations_completed', 'N/A')}")
                
                # Return base64 image as data URL
                image_data = result["imageData"]
                data_url = f"data:image/png;base64,{image_data}"
                
                return ImageGenerationResponse(
                    success=True,
                    imagePath=data_url
                )
            else:
                logger.error(f"Image generation failed for image #{request.imageNumber}: {result.get('error', 'Unknown error')}")
                return ImageGenerationResponse(
                    success=False,
                    error=result.get("error", "Unknown error occurred")
                )
                
        except Exception as e:
            logger.error(f"Controller error for image #{request.imageNumber}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
