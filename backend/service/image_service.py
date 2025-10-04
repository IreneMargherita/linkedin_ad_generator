import os
import base64
import logging
from openai import OpenAI
from dotenv import load_dotenv
from dto.ad_form_dto import AdFormData
from prompts.ad_generation_prompt import build_linkedin_ad_prompt
from prompts.ad_branding_prompt import build_branding_extraction_prompt
from utils.branding_service import BrandService

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logger = logging.getLogger(__name__)


class ImageService:
    """Service for handling image generation using OpenAI gpt-image-1"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.branding_service = BrandService()

    def generate_ad_image(self, form_data: AdFormData, style: str, image_number: int) -> dict:
        """
        Generate a LinkedIn ad image using gpt-image-1 with refinement loop
        
        Args:
            form_data: Form data from the frontend
            style: Style description for the image
            image_number: Image number for tracking
            
        Returns:
            dict with success status, base64 image data or error message
        """
        logger.info(f"Starting image generation for image #{image_number}")
        logger.debug(f"Form data - Product: {form_data.productName}, Audience: {form_data.audience}")
 
        try:       
            branding_context = build_branding_extraction_prompt(form_data.companyUrl)
            prompt = build_linkedin_ad_prompt(
                company_url=form_data.companyUrl,
                product_name=form_data.productName,
                business_value=form_data.businessValue,
                audience=form_data.audience,
                body_text=form_data.bodyText,
                footer_text=form_data.footerText
            )
            
            # Add style and branding context to the prompt
            prompt += f"""
STYLE REQUIREMENTS: {style}
{branding_context}
"""
            

            # Generate image using gpt-image-1 with LinkedIn ad dimensions
            logger.info("Calling OpenAI gpt-image-1 API")
            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
            )
            
            logger.info("OpenAI API response received successfully")
            # Get base64 image data
            image_base64 = response.data[0].b64_json
            logger.info(f"Image generated successfully for image #{image_number} (base64 length: {len(image_base64)})")
            
            return {
                "success": True,
                "imageData": image_base64,
                "imageNumber": image_number,
                "prompt": prompt  
            }
            
        except Exception as e:
            logger.error(f"Error generating image #{image_number}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
   
    
  

