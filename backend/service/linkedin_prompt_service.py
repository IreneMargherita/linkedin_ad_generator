import logging
from dto.ad_form_dto import AdFormData
from prompts.ad_generation_prompt import build_linkedin_ad_prompt
from prompts.ad_branding_prompt import build_branding_extraction_prompt
from interfaces.prompt_service_interface import PromptServiceInterface

logger = logging.getLogger(__name__)

class LinkedInPromptService(PromptServiceInterface):
    """Prompt builder specialized for LinkedIn ad image generation."""

    def build_prompt(self, form_data: AdFormData, style: str) -> str:
        logger.info("Building LinkedIn ad prompt for image generation.")

        branding_context = build_branding_extraction_prompt(form_data.companyUrl)
        base_prompt = build_linkedin_ad_prompt(
            company_url=form_data.companyUrl,
            product_name=form_data.productName,
            business_value=form_data.businessValue,
            audience=form_data.audience,
            body_text=form_data.bodyText,
            footer_text=form_data.footerText
        )

        return (
            f"{base_prompt}\n\n"
            f"STYLE REQUIREMENTS: {style}\n"
            f"{branding_context}"
        )
