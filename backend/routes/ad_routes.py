import logging
from fastapi import APIRouter
from dto.ad_form_dto import ImageGenerationRequest, ImageGenerationResponse
from controller.ad_controller import AdController

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ads", tags=["ads"])

# Create controller instance
ad_controller = AdController()
logger.info("Ad controller initialized")


@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    Generate a LinkedIn ad image based on form data
    
    - **formData**: Form data from the frontend (company, product, etc.)
    - **style**: Style description for the image
    - **imageNumber**: Image number for tracking
    """
    logger.info(f"POST /api/ads/generate-image - Image #{request.imageNumber}")
    logger.debug(f"Request data - Product: {request.formData.productName}, Style: {request.style}")
    return await ad_controller.generate_image(request)




