# app/dependencies/ad_dependencies.py

import logging
from controller.ad_controller import AdController
from dependencies.image_service_dependencies import get_Linkedin_openai_image_service
from fastapi import Depends
from service.image_service import ImageService

logger = logging.getLogger(__name__)

def get_ad_controller(image_service: ImageService = Depends(get_Linkedin_openai_image_service)) -> AdController:
    """Factory that injects ImageService into AdController."""
    return AdController(image_service=image_service)
