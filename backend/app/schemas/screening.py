
from pydantic import BaseModel, Field


class ScreeningRequest(BaseModel):
    signs: list[str] = Field(default_factory=list)
