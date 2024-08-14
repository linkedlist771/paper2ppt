from typing import Union, Any
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

from src.paper2ppt.configs.settings import get_settings
from src.paper2ppt.prompt_builder.output_language import OutputLanguage


class BasePrompt(BaseModel, ABC):
    # base_prompt: str = Field(..., description="Base prompt text")
    output_language: OutputLanguage = Field(
        default=get_settings().OUTPUT_LANGUAGE,
        description="Output language for the prompt",
    )

    @abstractmethod
    async def render_prompt(self) -> Union[str, Any]:
        raise NotImplementedError("Method render_prompt not implemented")
