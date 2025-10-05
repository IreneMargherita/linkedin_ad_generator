from abc import ABC, abstractmethod
from dto.ad_form_dto import AdFormData

class PromptServiceInterface(ABC):
    """Abstract interface for building prompts."""

    @abstractmethod
    def build_prompt(self, form_data: AdFormData, style: str) -> str:
        pass
