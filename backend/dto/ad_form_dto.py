from pydantic import BaseModel
from typing import Optional


class AdFormData(BaseModel):
 
    companyUrl: str
    productName: str
    businessValue: str
    audience: str
    bodyText: str
    footerText: str


class ImageGenerationRequest(BaseModel):
   
    formData: AdFormData
    style: str
    imageNumber: int


class ImageGenerationResponse(BaseModel):
    
    success: bool
    imagePath: Optional[str] = None
    error: Optional[str] = None

