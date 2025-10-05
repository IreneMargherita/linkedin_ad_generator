import logging
from fastapi import APIRouter, Depends
from dto.ad_form_dto import ImageGenerationRequest, ImageGenerationResponse
from controller.ad_controller import AdController
from dependencies.ad_controller_dependencies import get_ad_controller

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ads", tags=["ads"])

@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest,ad_controller:AdController=Depends(get_ad_controller)):
    logger.info(f"POST /api/ads/generate-image - Image #{request.imageNumber}")
    logger.debug(f"Request data - Product: {request.formData.productName}, Style: {request.style}")
    return await ad_controller.generate_image(request)




